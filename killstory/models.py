"""Models for the killstory application.

This module defines models for storing killmail information,
including killmails, victims, attackers, and associated items.
"""

from django.db import models


# Table principale pour chaque killmail
class Killmail(models.Model):
    """Model for storing main killmail information, including time, location, and identifiers."""

    killmail_id = models.IntegerField(primary_key=True)
    killmail_time = models.DateTimeField()
    solar_system_id = models.IntegerField()
    moon_id = models.IntegerField(null=True, blank=True)
    war_id = models.IntegerField(null=True, blank=True)

    # Position
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    position_z = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "killmail"

    def __str__(self):
        return f"Killmail {self.killmail_id}"


# Table pour enregistrer les détails de la victime dans le killmail
class Victim(models.Model):
    """Model for storing victim details within a killmail, such as character and damage taken."""

    killmail = models.OneToOneField(
        Killmail, on_delete=models.CASCADE, related_name="victim"
    )
    alliance_id = models.IntegerField(null=True, blank=True)
    character_id = models.IntegerField(null=True, blank=True)
    corporation_id = models.IntegerField(null=True, blank=True)
    faction_id = models.IntegerField(null=True, blank=True)
    damage_taken = models.IntegerField()
    ship_type_id = models.IntegerField()

    class Meta:
        db_table = "victim"

    def __str__(self):
        return f"Victim {self.character_id} in Killmail {self.killmail.killmail_id}"


# Table pour enregistrer les attaquants associés à chaque killmail
class Attacker(models.Model):
    """Model for storing attacker information, including damage done and whether they landed the final blow."""

    killmail = models.ForeignKey(
        Killmail, on_delete=models.CASCADE, related_name="attackers"
    )
    alliance_id = models.IntegerField(null=True, blank=True)
    character_id = models.IntegerField(null=True, blank=True)
    corporation_id = models.IntegerField(null=True, blank=True)
    faction_id = models.IntegerField(null=True, blank=True)
    damage_done = models.IntegerField()
    final_blow = models.BooleanField()
    security_status = models.FloatField()
    ship_type_id = models.IntegerField()
    weapon_type_id = models.IntegerField()

    class Meta:
        db_table = "attacker"

    def __str__(self):
        return f"Attacker {self.character_id} for Killmail {self.killmail.killmail_id}"


# Table pour les items possédés par la victime et détruits ou perdus
class VictimItem(models.Model):
    """Model for storing items owned by the victim and either destroyed or dropped in the killmail."""

    victim = models.ForeignKey(Victim, on_delete=models.CASCADE, related_name="items")
    item_type_id = models.IntegerField()
    flag = models.IntegerField()
    quantity_destroyed = models.BigIntegerField(null=True, blank=True)
    quantity_dropped = models.BigIntegerField(null=True, blank=True)
    singleton = models.IntegerField()

    class Meta:
        db_table = "victim_item"

    def __str__(self):
        return f"Item {self.item_type_id} for Victim {self.victim.character_id}"


# Table pour les sous-items (contenus dans un item de la victime)
class VictimContainedItem(models.Model):
    """Model for storing sub-items contained within a victim's item, with details on quantity and status."""

    parent_item = models.ForeignKey(
        VictimItem, on_delete=models.CASCADE, related_name="contained_items"
    )
    item_type_id = models.IntegerField()
    flag = models.IntegerField()
    quantity_destroyed = models.BigIntegerField(null=True, blank=True)
    quantity_dropped = models.BigIntegerField(null=True, blank=True)
    singleton = models.IntegerField()

    class Meta:
        db_table = "victim_contained_item"

    def __str__(self):
        return (
            f"ContainedItem {self.item_type_id} in Item {self.parent_item.item_type_id}"
        )
