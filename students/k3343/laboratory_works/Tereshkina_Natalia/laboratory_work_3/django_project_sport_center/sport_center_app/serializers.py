from rest_framework import serializers
from .models import *


class SportsmenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sportsman
        fields = "__all__"


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = "__all__"


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class SportHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportHall
        fields = "__all__"


class EquipmentOfSportHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentOfSportHall
        fields = "__all__"


class SportSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportSection
        fields = "__all__"


class SportSectionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportSection
        fields = ['title']


class SportSectionCoachesSerializer(serializers.ModelSerializer):
    section = SportSectionTitleSerializer(required=True)

    class Meta:
        model = SportSectionCoaches
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    sport_section = SportSectionTitleSerializer(required=True)
    sport_hall = SportHallSerializer(required=True)

    class Meta:
        model = Schedule
        fields = "__all__"
