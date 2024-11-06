# killstory/tasks.py

import time
import logging
import requests
from celery import shared_task
from django.db import transaction, IntegrityError
from allianceauth.eveonline.models import EveCharacter
from allianceauth.authentication.models import CharacterOwnership
from .models import Killmail, Victim, Attacker, VictimItem, VictimContainedItem
from .app_settings import KILLSTORY_API_LIST_ENDPOINT, KILLSTORY_API_DETAIL_ENDPOINT, KILLSTORY_BATCH_SIZE, KILLSTORY_RETRY_LIMIT

logger = logging.getLogger(__name__)

@shared_task
def populate_killmails():
    """Populate killmails for owned characters asynchronously."""
    character_ids = EveCharacter.objects.filter(
        id__in=CharacterOwnership.objects.values_list('character_id', flat=True)
    ).values_list('character_id', flat=True)

    batch = []
    for character_id in character_ids:
        try:
            killmails = fetch_killmail_list(character_id)
            if not killmails:
                continue

            for kill_id, kill_hash in killmails.items():
                killmail_data = fetch_killmail_details(kill_id, kill_hash)
                if not killmail_data:
                    continue
                killmail = create_killmail_instance(killmail_data)
                batch.append((killmail, killmail_data))

                if len(batch) >= KILLSTORY_BATCH_SIZE:
                    save_batch(batch)
                    batch.clear()

        except requests.HTTPError as e:
            logger.error("Request error for character_id %s: %s", character_id, e)
        except IntegrityError as e:
            logger.error("Integrity error for character_id %s: %s", character_id, e)

    if batch:
        save_batch(batch)
    logger.info("Population completed")

# Helper functions
def fetch_killmail_list(character_id):
    try:
        response = make_request(KILLSTORY_API_LIST_ENDPOINT.format(character_id))
        if response and response.status_code == 404:
            logger.warning("Character_id %s not found, skipping.", character_id)
            return {}
        return response.json() if response else {}
    except requests.RequestException as e:
        logger.error("Error fetching killmails for character_id %s: %s", character_id, e)
        return {}

def fetch_killmail_details(kill_id, kill_hash):
    response = make_request(KILLSTORY_API_DETAIL_ENDPOINT.format(kill_id, kill_hash))
    return response.json() if response else {}

def make_request(url):
    retries = 0
    while retries < KILLSTORY_RETRY_LIMIT:
        try:
            response = requests.get(url, timeout=10)
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

def create_killmail_instance(data):
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

def save_batch(batch):
    with transaction.atomic():
        for killmail, killmail_data in batch:
            try:
                killmail.save()
                if "victim" in killmail_data:
                    create_victim_instance(killmail, killmail_data['victim'])
                for attacker_data in killmail_data.get('attackers', []):
                    create_attacker_instance(killmail, attacker_data)
            except IntegrityError:
                continue

def create_victim_instance(killmail, victim_data):
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
        create_victim_item_instance(victim, item_data)

def create_attacker_instance(killmail, attacker_data):
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

def create_victim_item_instance(victim, item_data):
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
        create_contained_item_instance(item, contained_item_data)

def create_contained_item_instance(parent_item, contained_item_data):
    contained_item = VictimContainedItem(
        parent_item=parent_item,
        item_type_id=contained_item_data['item_type_id'],
        flag=contained_item_data['flag'],
        quantity_destroyed=contained_item_data.get('quantity_destroyed'),
        quantity_dropped=contained_item_data.get('quantity_dropped'),
        singleton=contained_item_data['singleton']
    )
    contained_item.save()
