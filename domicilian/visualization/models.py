# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnnualIncome(models.Model):
    zipcode = models.ForeignKey("Zipcode", models.DO_NOTHING)
    avg_annual_income = models.IntegerField()
    median_annual_income = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "annual_income"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class Business(models.Model):
    zipcode = models.ForeignKey("Zipcode", models.DO_NOTHING)
    address = models.CharField(max_length=150, blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    categories = models.CharField(max_length=400, blank=True, null=True)
    business_id = models.CharField(max_length=100)
    name = models.CharField(max_length=300)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "business"


class City(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey("State", models.DO_NOTHING)
    county = models.ForeignKey("County", models.DO_NOTHING)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "city"
        unique_together = (("name", "county", "state"),)


class CityHomeSaleInventory(models.Model):
    city = models.ForeignKey(City, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    total = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "city_home_sale_inventory"


class CityMedianPrice(models.Model):
    city = models.ForeignKey(City, models.DO_NOTHING)
    home_type = models.ForeignKey("HomeType", models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    list_price = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "city_median_price"


class CitySaleCount(models.Model):
    city = models.ForeignKey(City, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    total = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "city_sale_count"


class CityTimeseries(models.Model):
    city = models.ForeignKey(City, models.DO_NOTHING)
    home_type = models.ForeignKey("HomeType", models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    zillow_id = models.IntegerField()
    index_value = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "city_timeseries"


class County(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey("State", models.DO_NOTHING)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "county"
        unique_together = (("name", "state"),)


class CountyHomeSaleInventory(models.Model):
    county = models.ForeignKey(County, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    total = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "county_home_sale_inventory"


class CountyMedianPrice(models.Model):
    county = models.ForeignKey(County, models.DO_NOTHING)
    home_type = models.ForeignKey("HomeType", models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    list_price = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "county_median_price"


class CountySaleCount(models.Model):
    county = models.ForeignKey(County, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    total = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "county_sale_count"


class CountyTimeseries(models.Model):
    county = models.ForeignKey(County, models.DO_NOTHING)
    home_type = models.ForeignKey("HomeType", models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    index_value = models.IntegerField(blank=True, null=True)
    zillow_id = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "county_timeseries"


class CrimeData(models.Model):
    zipcode = models.ForeignKey("Zipcode", models.DO_NOTHING)
    violent_crime = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    property_crime = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "crime_data"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey("UsersUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class HomeType(models.Model):
    type = models.CharField(max_length=150)
    feature = models.CharField(max_length=150)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "home_type"
        unique_together = (("type", "feature"),)


class Neighborhood(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey("State", models.DO_NOTHING)
    county = models.ForeignKey(County, models.DO_NOTHING)
    city = models.ForeignKey(City, models.DO_NOTHING)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "neighborhood"
        unique_together = (("name", "state", "county", "city"),)


class NeighborhoodMedianPrice(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, models.DO_NOTHING)
    home_type = models.ForeignKey(HomeType, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    list_price = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "neighborhood_median_price"


class NeighborhoodTimeseries(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, models.DO_NOTHING)
    home_type = models.ForeignKey(HomeType, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    zillow_id = models.IntegerField()
    index_value = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "neighborhood_timeseries"


class PredictedPrices(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    schooldigger_rating = models.FloatField(blank=True, null=True)
    average_standard_score = models.FloatField(blank=True, null=True)
    county_id = models.FloatField(blank=True, null=True)
    violent_crime = models.FloatField(blank=True, null=True)
    property_crime = models.FloatField(blank=True, null=True)
    home_type_id = models.FloatField(blank=True, null=True)
    year = models.BigIntegerField(blank=True, null=True)
    month = models.FloatField(blank=True, null=True)
    y_pred = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predicted_prices'


class SchoolData(models.Model):
    zipcode = models.ForeignKey("Zipcode", models.DO_NOTHING)
    school_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    schooldigger_rating = models.IntegerField(blank=True, null=True)
    average_standard_score = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "school_data"


class State(models.Model):
    state_code = models.CharField(unique=True, max_length=2)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "state"


class StateHomeSaleInventory(models.Model):
    state = models.ForeignKey(State, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    total = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "state_home_sale_inventory"


class StateMedianPrice(models.Model):
    state = models.ForeignKey(State, models.DO_NOTHING)
    home_type = models.ForeignKey(HomeType, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    list_price = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "state_median_price"


class StateSaleCount(models.Model):
    state = models.ForeignKey(State, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    total = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "state_sale_count"


class StateTimeseries(models.Model):
    state = models.ForeignKey(State, models.DO_NOTHING)
    home_type = models.ForeignKey(HomeType, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    zillow_id = models.IntegerField()
    index_value = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "state_timeseries"


class UsersUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.TextField(unique=True)  # This field type is a guess.
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "users_user"


class UsersUserGroups(models.Model):
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "users_user_groups"
        unique_together = (("user", "group"),)


class UsersUserUserPermissions(models.Model):
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "users_user_user_permissions"
        unique_together = (("user", "permission"),)


class ZipHomeSaleInventory(models.Model):
    zipcode = models.ForeignKey("Zipcode", models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    total = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "zip_home_sale_inventory"


class ZipMedianPrice(models.Model):
    zipcode = models.ForeignKey("Zipcode", models.DO_NOTHING)
    home_type = models.ForeignKey(HomeType, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    list_price = models.IntegerField(blank=True, null=True)
    sale_price = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "zip_median_price"


class ZipTimeseries(models.Model):
    zipcode = models.ForeignKey("Zipcode", models.DO_NOTHING)
    home_type = models.ForeignKey(HomeType, models.DO_NOTHING)
    year_month = models.CharField(max_length=7)
    zillow_id = models.IntegerField()
    index_value = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "zip_timeseries"


class Zipcode(models.Model):
    zip_code = models.CharField(max_length=150)
    state = models.ForeignKey(State, models.DO_NOTHING)
    county = models.ForeignKey(County, models.DO_NOTHING)
    city = models.ForeignKey(City, models.DO_NOTHING)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "zipcode"
        unique_together = (("zip_code", "state", "county", "city"),)
