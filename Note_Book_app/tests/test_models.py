from django.test import TestCase
from django.urls import reverse
from Note_Book_app.models import Note
from .django_modelfield_tests_funcs import *
import datetime
import decimal
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid 
import pytz
from freezegun import freeze_time


class Backend_tests(TestCase):
    """this class is for backend tests and tests the backend functionality."""
    def setUp(self): #in this func you need to specify which field your model is using.if for example you are using CharField just change the CharField boolean variable to True.       
        self.BigIntegerField=False
        self.BinaryField=False
        self.BooleanField=False
        self.CharField=True
        self.DateField=False
        # self.DateTimeField=True
        self.DecimalField=False
        self.DurationField=False
        self.EmailField=False
        self.FileField=False
        self.ImageField=False
        self.FloatField=False
        self.IntegerField=False
        self.GenericIPAddressField=False
        self.PositiveIntegerField=False
        self.PositiveSmallIntegerField=False
        self.SlugField=False
        self.SmallIntegerField=False
        self.TextField=True
        self.TimeField=False
        self.URLField=False
        self.UUIDField=False
        self.PositiveBigIntegerField=False
        field_values={}
        
        if self.BigIntegerField:
            BigIntegerField_value=10000000
            BigIntegerField_name='BigIntegerField' #please input your field_name here.
            field_values[BigIntegerField_name]=BigIntegerField_value


        if self.BinaryField:
            BinaryField_value=0
            BinaryField_name='BinaryField'
            field_values[BinaryField_name]=BinaryField_value

        if self.BooleanField:
            BooleanField_value=False
            BooleanField_name='BooleanField'
            field_values[BooleanField_name]=BooleanField_value

        if self.CharField:
            CharField_value='test'
            CharField_name='name'
            field_values[CharField_name]=CharField_value

        if self.DateField:
            DateField_value=datetime.date(1997, 10, 19)
            DateField_name='DateField'
            field_values[DateField_name]=DateField_value

        # if self.DateTimeField:
        #     DateTimeField_value=datetime(2015, 10, 11, 23, 55, 59, 342380) 
        #     DateTimeField_name='Published_at'
        #     field_values[DateTimeField_name]=DateTimeField_value

        if self.DecimalField:
            DecimalField_value=decimal.Decimal(9.53) 
            DecimalField_name='DecimalField'
            field_values[DecimalField_name]=DecimalField_value

        if self.DurationField:
            DurationField_value=datetime.timedelta(days =-1, seconds = 68400)
            DurationField_name='DurationField'
            field_values[DurationField_name]=DurationField_value

        if self.EmailField:
            EmailField_value='example@email.com'
            EmailField_name='EmailField'
            field_values[EmailField_name]=EmailField_value

        if self.FileField:
            FileField_value=SimpleUploadedFile(
            name="test_file.txt",
            content=b"Hello, this is a test file!",
            content_type="text/plain"
        )
            FileField_name='FileField'
            field_values[FileField_name]=FileField_value

        if self.ImageField:
            ImageField_value= SimpleUploadedFile(
            name="test_image.jpg",
            content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x0A\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B",
            content_type="image/jpeg"
        )
            ImageField_name='ImageField'
            field_values[ImageField_name]=ImageField_value

        if self.FloatField:
            FloatField_value=float(21.89)
            FloatField_name='FloatField'
            field_values[FloatField_name]=FloatField_value

        if self.IntegerField:
            IntegerField_value=10
            IntegerField_name='IntegerField'
            field_values[IntegerField_name]=IntegerField_value

        if self.GenericIPAddressField:
            GenericIPAddressField_value="0.0.0.0"
            GenericIPAddressField_name='GenericIPAddressField'
            field_values[GenericIPAddressField_name]=GenericIPAddressField_value

        if self.PositiveIntegerField:
            positiveintegerfield_value=2147483647
            PositiveIntegerField_name='PositiveIntegerField'
            field_values[PositiveIntegerField_name]=positiveintegerfield_value

        if self.PositiveSmallIntegerField:
            PositiveSmallIntegerField_value=32767
            PositiveSmallIntegerField_name='PositiveSmallIntegerField'
            field_values[PositiveSmallIntegerField_name]=PositiveSmallIntegerField_value

        if self.SlugField:
            SlugField_value="my-custom-slug"
            SlugField_name='SlugField'
            field_values[SlugField_name]=SlugField_value

        if self.SmallIntegerField:
            SmallIntegerField_value=-32768
            SmallIntegerField_name='SmallIntegerField'
            field_values[SmallIntegerField_name]=SmallIntegerField_value

        if self.TextField:
            TextField_value='test'
            TextField_name='note'
            field_values[TextField_name]=TextField_value

        if self.TimeField:
            TimeField_value=datetime.time(10, 33, 45) 
            TimeField_name='TimeField'
            field_values[TimeField_name]=TimeField_value

        if self.URLField:
            URLField_value='https://example.com/'
            URLField_name='URLField'
            field_values[URLField_name]=URLField_value

        if self.UUIDField:
            UUIDField_value=uuid.uuid4()
            UUIDField_name='UUIDField'
            field_values[UUIDField_name]=UUIDField_value

        if self.PositiveBigIntegerField:
            PositiveBigIntegerField_value=9223372036854775807
            PositiveBigIntegerField_name='PositiveBigIntegerField'
            field_values[PositiveBigIntegerField_name]=PositiveBigIntegerField_value
        self.field_values=field_values
        self.ob=Note.objects.create(**field_values)

    def test_field_object_created_sucssefuly_class_from_django_modelfield_tests_funcs(self): # this func calls another class with its func in the django_modelfield_tests_funcs.py to test model objects data.
        field_object_created_sucssefuly(Model_name=Note,Model_objects=self.ob).test_Model_object_creadted_sucssefuly(**self.field_values)
        field_object_created_sucssefuly(Model_name=Note,Model_objects=self.ob).test_Model_object_data_saved_correctly(**self.field_values)

    def test_publication_date_is_set_on_creation(self): #Verifies that the timestamp is set upon object creation.
        Note.objects.create(name="name of the note",note= "this is the note.")
        initial_datetime = datetime.datetime(year=1971, month=1, day=1,hour=1, minute=1, second=1,tzinfo=pytz.UTC)
        with freeze_time(initial_datetime) as frozen_datetime:
            Note.objects.create(name="name of the note",note= "this is the note.")
            self.assertEqual(Note.objects.last().Published_at.timestamp(),initial_datetime.timestamp())
