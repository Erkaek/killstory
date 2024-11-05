"""
Management command to populate killmails for owned characters from the EVE Online API.
"""

import time
import logging
import requests
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from allianceauth.eveonline.models import EveCharacter
from allianceauth.authentication.models import CharacterOwnership
from killstory.models import Killmail, Victim, Attacker, VictimItem, VictimContainedItem

# API Endpoints
KILLMAIL_LIST_ENDPOINT = "https://killstory.soeo.fr/{}.json"
KILLMAIL_DETAIL_ENDPOINT = "https://esi.evetech.net/latest/killmails/{}/{}"

BATCH_SIZE = 100
RETRY_LIMIT = 5
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Django management command to populate killmails data for owned characters."""
    help = 'Populate killmails data for owned characters'

    def handle(self, *args, **options):
        """Main handler for the command execution."""
        character_ids = EveCharacter.objects.filter(
            id__in=CharacterOwnership.objects.values_list('character_id', flat=True)
        ).values_list('character_id', flat=True)

        batch = []
        for character_id in character_ids:
            try:
                killmails = self.fetch_killmail_list(character_id)
                if not killmails:
                    continue

                for kill_id, kill_hash in killmails.items():
                    killmail_data = self.fetch_killmail_details(kill_id, kill_hash)
                    if not killmail_data:
                        continue
                    killmail = self.create_killmail_instance(killmail_data)
                    batch.append((killmail, killmail_data))

                    if len(batch) >= BATCH_SIZE:
                        self.save_batch(batch)
                        batch.clear()

            except requests.HTTPError as e:
                logger.error("Request error for character_id %s: %s", character_id, e)
            except IntegrityError as e:
                logger.error("Integrity error for character_id %s: %s", character_id, e)

        if batch:
            self.save_batch(batch)
        logger.info("Population completed")

    def fetch_killmail_list(self, character_id):
        """Fetches the list of killmails for a given character."""
        try:
            response = self.make_request(KILLMAIL_LIST_ENDPOINT.format(character_id))
            if response and response.status_code == 404:
                logger.warning("Character_id %s not found, skipping.", character_id)
                return {}
            return response.json() if response else {}
        except requests.RequestException as e:
            logger.error("Error fetching killmails for character_id %s: %s", character_id, e)
            return {}

    def fetch_killmail_details(self, kill_id, kill_hash):
        """Fetches details for a specific killmail."""
        response = self.make_request(KILLMAIL_DETAIL_ENDPOINT.format(kill_id, kill_hash))
        return response.json() if response else {}

    def make_request(self, url):
        """Makes a request with retries and error handling."""
        retries = 0
        while retries < RETRY_LIMIT:
            try:
                response = requests.get(url, timeout=10)  # Added timeout here
                if response.status_code in [304, 400, 422]:
                    return None
                if response.status_code in [420, 500, 503, 504]:
                    time.sleep(2 ** retries)
                else:
                    response.raise_for_status()
                    return response
            except requests.RequestException as e:
                logger.error("Network error: %s, attempt %d", e, retries + 1)
            retries += 1

        logger.error("Retry limit reached, moving to next killmail.")
        return None

    def create_killmail_instance(self, data):
        """Creates a killmail instance from API data."""
        return Killmail(
            killmail_id=data['killmail_id'],
            killmail_time=data['killmail_time'],
            solar_system_id=data['solar_system_id'],
            moon_id=data.get('moon_id'),
            war_id=data.get('war_id'),
            position_x=data.get('position', {}).get('x'),
            position_y=data.get('position', {}).get('y'),
            position_z=data.get('position', {}).get('z')
        )

    def save_batch(self, batch):
        """Saves a batch of killmails in a transaction."""
        with transaction.atomic():
            for killmail, killmail_data in batch:
                try:
                    killmail.save()
                    if "victim" in killmail_data:
                        self.create_victim_instance(killmail, killmail_data['victim'])
                    for attacker_data in killmail_data.get('attackers', []):
                        self.create_attacker_instance(killmail, attacker_data)
                except IntegrityError:
                    continue

    def create_victim_instance(self, killmail, victim_data):
        """Creates a victim instance associated with a killmail."""
        victim = Victim(
            killmail=killmail,
            alliance_id=victim_data.get('alliance_id'),
            character_id=victim_data.get('character_id'),
            corporation_id=victim_data.get('corporation_id'),
            faction_id=victim_data.get('faction_id'),
            damage_taken=victim_data['damage_taken'],
            ship_type_id=victim_data['ship_type_id']
        )
        victim.save()
        for item_data in victim_data.get('items', []):
            self.create_victim_item_instance(victim, item_data)

    def create_attacker_instance(self, killmail, attacker_data):
        """Creates an attacker instance for a killmail."""
        attacker = Attacker(
            killmail=killmail,
            alliance_id=attacker_data.get('alliance_id'),
            character_id=attacker_data.get('character_id'),
            corporation_id=attacker_data.get('corporation_id'),
            faction_id=attacker_data.get('faction_id'),
            damage_done=attacker_data['damage_done'],
            final_blow=attacker_data['final_blow'],
            security_status=attacker_data['security_status'],
            ship_type_id=attacker_data['ship_type_id'],
            weapon_type_id=attacker_data.get('weapon_type_id')
        )
        attacker.save()

    def create_victim_item_instance(self, victim, item_data):
        """Creates an item instance for the victim."""
        item = VictimItem(
            victim=victim,
            item_type_id=item_data['item_type_id'],
            flag=item_data['flag'],
            quantity_destroyed=item_data.get('quantity_destroyed'),
            quantity_dropped=item_data.get('quantity_dropped'),
            singleton=item_data['singleton']
        )
        item.save()
        for contained_item_data in item_data.get('items', []):
            self.create_contained_item_instance(item, contained_item_data)

    def create_contained_item_instance(self, parent_item, contained_item_data):
        """Creates a contained item instance for a victim item."""
        contained_item = VictimContainedItem(
            parent_item=parent_item,
            item_type_id=contained_item_data['item_type_id'],
            flag=contained_item_data['flag'],
            quantity_destroyed=contained_item_data.get('quantity_destroyed'),
            quantity_dropped=contained_item_data.get('quantity_dropped'),
            singleton=contained_item_data['singleton']
        )
        contained_item.save()
