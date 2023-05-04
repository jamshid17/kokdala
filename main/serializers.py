from datetime import datetime, date
from rest_framework import serializers
from .models import Mahalla, Rais, Sector, Xonadon, Person 


class MainStatsSerializer(serializers.Serializer):
    mahalla_count = serializers.IntegerField()
    population_count = serializers.IntegerField()
    households_with_problems = serializers.IntegerField()
    households_without_problems = serializers.IntegerField()
 


class MahallaInfoSerializer(serializers.ModelSerializer):
    without_problem_households = serializers.SerializerMethodField()
    in_process_organish_households = serializers.SerializerMethodField()
    finished_organish_households = serializers.SerializerMethodField()

    class Meta:
        model = Mahalla
        fields = [
            'id',
            'name',
            'households_count',
            'population',
            'without_problem_households',
            'in_process_organish_households',
            'finished_organish_households',
        ]

    def get_without_problem_households(self, obj):
        return_sum = 0
        households = obj.xonadon.all()
        for household in households:
            if household.organish.count() == 0:
                return_sum += 1
        return return_sum       

    def get_in_process_organish_households(self, obj):
        return_sum = 0
        households = obj.xonadon.all()
        for household in households:
            organishlar = household.organish.all()
            for organish in organishlar:
                if organish.hal_qilish_holati == "Davom etayapti":
                    return_sum += 1
                    break 
        return return_sum       

    def get_finished_organish_households(self, obj):
        return_sum = 0
        households = obj.xonadon.all()
        for household in households:
            organishlar = household.organish.all()
            have_finished_organish = True
            for organish in organishlar:
                if organish.hal_qilish_holati == "Davom etayapti":
                    have_finished_organish = False
                    break 
            if not have_finished_organish:
                return_sum += 1

        return return_sum       


class SectorInfoSerializer(serializers.ModelSerializer):
    mahalla = MahallaInfoSerializer(many=True)

    class Meta:
        model = Sector
        fields = [
            'number',
            'mahalla'
            ]


class RaisInfoSerializer(serializers.ModelSerializer):
    mahalla_name = serializers.SerializerMethodField()

    class Meta:
        model = Rais
        fields = [
            "first_name", 
            "last_name",
            "middle_name",
            "phone_number",
            "email",
            "image",
            "mahalla_name"
        ]

    def get_mahalla_name(self, obj):
        return obj.mahalla.name



class MahallaIdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mahalla
        fields = [
            "id"
        ]

class XonadonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Xonadon
        fields = [
            'address'
        ]


class DetailedXonadonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Xonadon
        fields = [
            'address',
        ]

    def to_representation(self, instance):
        now = date.today()
        representation = super().to_representation(instance)
        owner = instance.person.get(is_egasi=True)
        representation['owner_name'] = f"{owner.first_name} {owner.last_name}"
        representation['owner_phone_number'] = f"+{owner.phone_number.country_code} {owner.phone_number.national_number}"
        representation['owner_age'] = (now - owner.birth_date).days // 365
        return representation


class PersonSerializer(serializers.ModelSerializer):
    old = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "old",
            "phone_number",
            "is_egasi",
            "address",
            
        ]

    def get_old(self, obj):
        farq = datetime.now().date() - obj.birth_date
        old = int(farq.days/365.2425)
        return old
    
    def get_address(self, obj):
        return obj.household.address