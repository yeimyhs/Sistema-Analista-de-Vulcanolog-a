from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from .models import Alert, Alertconfiguration, Blob, Eventtype, History, Imagesegmentation, Mask, Meteorologicaldata, Station, Temporaryseries, UserP, Volcano

# Create your tests here.
from django.test import TestCase
from .models import Alert, Alertconfiguration, Blob, Eventtype

class AlertModelTestCase(TestCase):
    def setUp(self):
        Alert.objects.create(
            messagealert="Test Message",
            statealert=1,
        )

    def test_alert_creation(self):
        alert = Alert.objects.get(messagealert="Test Message")
        self.assertEqual(alert.statealert, 1)

class AlertconfigurationModelTestCase(TestCase):
    def setUp(self):
        Alertconfiguration.objects.create(
            altitudalertconf=100.0,
            statealertconf=2,
        )

    def test_alertconfiguration_creation(self):
        alertconf = Alertconfiguration.objects.get(altitudalertconf=100.0)
        self.assertEqual(alertconf.statealertconf, 2)

class BlobModelTestCase(TestCase):
    def setUp(self):
        Blob.objects.create(
            filenameblob="test_file.jpg",
            heightblob=200,
            stateblob=3,
        )

    def test_blob_creation(self):
        blob = Blob.objects.get(filenameblob="test_file.jpg")
        self.assertEqual(blob.heightblob, 200)

class EventtypeModelTestCase(TestCase):
    def setUp(self):
        Eventtype.objects.create(
            nameevent="Test Event",
            stateevent=4,
        )

    def test_eventtype_creation(self):
        eventtype = Eventtype.objects.get(nameevent="Test Event")
        self.assertEqual(eventtype.stateevent, 4)
