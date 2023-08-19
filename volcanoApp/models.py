# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Alert(models.Model):
    messagealert = models.TextField(db_column='messageAlert')  # Field name made lowercase.
    idalert = models.BigAutoField(db_column='idAlert', primary_key=True)  # Field name made lowercase.
    datecreationalert = models.TimeField(db_column='dateCreationAlert',auto_now_add=True)  # Field name made lowercase.
    statealert = models.IntegerField(db_column='stateAlert')  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano')  # Field name made lowercase.
    idalertconf = models.ForeignKey('Alertconfiguration', models.DO_NOTHING, db_column='idAlertConf')  # Field name made lowercase.
    startalert = models.SmallIntegerField(db_column='startAlert', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Alert'


class Alertconfiguration(models.Model):
    idalertconf = models.BigAutoField(db_column='idAlertConf', primary_key=True)  # Field name made lowercase.
    altitudalertconf = models.FloatField(db_column='altitudAlertConf')  # Field name made lowercase.
    statealertconf = models.IntegerField(db_column='stateAlertConf')  # Field name made lowercase.
    datecreationalertconf = models.TimeField(db_column='dateCreationAlertConf',auto_now_add=True)  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano', blank=True, null=True)  # Field name made lowercase.
    notificationalertconf = models.BigIntegerField(db_column='notificationAlertConf', blank=True, null=True)  # Field name made lowercase.
    messagetemplateconfalert = models.BigIntegerField(db_column='messageTemplateConfAlert', blank=True, null=True)  # Field name made lowercase.
    mensajeriaalertconf = models.SmallIntegerField(db_column='mensajeriaAlertConf', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'AlertConfiguration'


class Blob(models.Model):
    idblob = models.BigAutoField(db_column='idBlob', primary_key=True)  # Field name made lowercase.
    idmask = models.ForeignKey('Mask', models.DO_NOTHING, db_column='idMask')  # Field name made lowercase.
    starttimeblob = models.DateTimeField(db_column='startTimeBlob')  # Field name made lowercase.
    filenameblob = models.TextField(db_column='fileNameBlob')  # Field name made lowercase.
    directionblob = models.BigIntegerField(db_column='directionBlob')  # Field name made lowercase.
    heightblob = models.IntegerField(db_column='heightBlob')  # Field name made lowercase.
    stateblob = models.SmallIntegerField(db_column='stateBlob')  # Field name made lowercase.
    datecreationblob = models.DateTimeField(db_column='dateCreationBlob',auto_now_add=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Blob'


class Eventtype(models.Model):
    ideventtype = models.BigAutoField(db_column='idEventType', primary_key=True)  # Field name made lowercase.
    nameevent = models.CharField(db_column='nameEvent', max_length=126)  # Field name made lowercase.
    datecreationevent = models.DateTimeField(db_column='dateCreationEvent',auto_now_add=True)  # Field name made lowercase.
    stateevent = models.BigIntegerField(db_column='stateEvent')  # Field name made lowercase.

    class Meta:
        db_table = 'EventType'


class History(models.Model):
    idhistory = models.BigAutoField(db_column='idHistory', primary_key=True)  # Field name made lowercase.
    datemodificationhistory = models.DateTimeField(db_column='dateModificationHistory')  # Field name made lowercase.
    contentstringhistory = models.TextField(db_column='contentStringHistory')  # Field name made lowercase.
    statepermissionchangehistory = models.IntegerField(db_column='statePermissionChangeHistory')  # Field name made lowercase.
    datepermissionchangehistory = models.TimeField(db_column='datePermissionChangeHistory')  # Field name made lowercase.
    idtabletochangehistory = models.BigIntegerField(db_column='idTableToChangeHistory')  # Field name made lowercase.
    iduser = models.ForeignKey(User, models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.
    idregisterhistory = models.BigIntegerField(db_column='idRegisterHistory')  # Field name made lowercase.

    class Meta:
        db_table = 'History'


class Imagesegmentation(models.Model):
    idphoto = models.BigAutoField(db_column='idPhoto', primary_key=True)  # Field name made lowercase.
    urlimg = models.TextField(db_column='urlImg')  # Field name made lowercase.
    filenameimg = models.CharField(db_column='fileNameImg', max_length=128)  # Field name made lowercase.
    stateimg = models.SmallIntegerField(db_column='stateImg')  # Field name made lowercase.
    datecreationimg = models.DateTimeField(db_column='dateCreationImg',auto_now_add=True)  # Field name made lowercase.

    class Meta:
        db_table = 'ImageSegmentation'


class Mask(models.Model):
    idmask = models.BigAutoField(db_column='idMask', primary_key=True)  # Field name made lowercase.
    idphoto = models.ForeignKey(Imagesegmentation, models.DO_NOTHING, db_column='idPhoto')  # Field name made lowercase.
    starttimetmask = models.DateTimeField(db_column='startTimetMask')  # Field name made lowercase.
    filenametmask = models.TextField(db_column='fileNametMask')  # Field name made lowercase.
    perimetertmask = models.FloatField(db_column='perimetertMask')  # Field name made lowercase.
    xcentroidtmask = models.FloatField(db_column='xCentroidtMask')  # Field name made lowercase.
    ycentroidtmask = models.FloatField(db_column='yCentroidtMask')  # Field name made lowercase.
    directiontmask = models.TextField(db_column='directiontMask')  # Field name made lowercase.
    areatmask = models.FloatField(db_column='areatMask')  # Field name made lowercase.
    heightmask = models.FloatField(db_column='heightMask')  # Field name made lowercase.
    idstation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idStation')  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano')  # Field name made lowercase.

    class Meta:
        db_table = 'Mask'


class Meteorologicaldata(models.Model):
    starttimemet = models.DateTimeField(db_column='startTimeMet')  # Field name made lowercase.
    latitudemet = models.FloatField(db_column='latitudeMet')  # Field name made lowercase.
    longitudemet = models.FloatField(db_column='longitudeMet')  # Field name made lowercase.
    umet = models.FloatField(db_column='uMet')  # Field name made lowercase.
    vmet = models.FloatField(db_column='vMet')  # Field name made lowercase.
    speedmet = models.FloatField(db_column='speedMet')  # Field name made lowercase.
    directionmet = models.FloatField(db_column='directionMet')  # Field name made lowercase.
    temperaturemet = models.FloatField(db_column='temperatureMet')  # Field name made lowercase.
    geopotentialheightmet = models.FloatField(db_column='geopotentialHeightMet')  # Field name made lowercase.
    indmet = models.IntegerField(db_column='indMet')  # Field name made lowercase.
    jsonidmet = models.BigIntegerField(db_column='jsonIdMet')  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano', blank=True, null=True)  # Field name made lowercase.
    idtemporaryseries = models.ForeignKey('Temporaryseries', models.DO_NOTHING, db_column='idTemporarySeries', blank=True, null=True)  # Field name made lowercase.
    statemet = models.SmallIntegerField(db_column='stateMet')  # Field name made lowercase.
    datecreationmet = models.DateTimeField(db_column='dateCreationMet',auto_now_add=True)  # Field name made lowercase.
    idmetereorologicaldata = models.BigAutoField(db_column='idMetereorologicalData', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'MeteorologicalData'


class Station(models.Model):
    idstation = models.BigAutoField(db_column='idStation', primary_key=True)  # Field name made lowercase.
    standardnamestat = models.CharField(db_column='standardNameStat', max_length=64)  # Field name made lowercase.
    shortnamestat = models.CharField(db_column='shortNameStat', max_length=20)  # Field name made lowercase.
    longnamestat = models.CharField(db_column='longNameStat', max_length=126)  # Field name made lowercase.
    starttimestat = models.DateTimeField(db_column='startTimeStat')  # Field name made lowercase.
    latitudestat = models.FloatField(db_column='latitudeStat')  # Field name made lowercase.
    longitudestat = models.FloatField(db_column='longitudeStat')  # Field name made lowercase.
    altitudestat = models.FloatField(db_column='altitudeStat')  # Field name made lowercase.
    indstat = models.IntegerField(db_column='indStat')  # Field name made lowercase.
    statestat = models.IntegerField(db_column='stateStat')  # Field name made lowercase.
    datecreationstat = models.DateTimeField(db_column='dateCreationStat',auto_now_add=True)  # Field name made lowercase.
    typestat = models.SmallIntegerField(db_column='typeStat', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Station'


class Temporaryseries(models.Model):
    idtemporaryseries = models.BigAutoField(db_column='idTemporarySeries', primary_key=True)  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano')  # Field name made lowercase.
    idstation = models.ForeignKey(Station, models.DO_NOTHING, db_column='idStation')  # Field name made lowercase.
    ideventtype = models.ForeignKey(Eventtype, models.DO_NOTHING, db_column='idEventType')  # Field name made lowercase.
    meantempser = models.FloatField(db_column='meanTempSer')  # Field name made lowercase.
    variancetempser = models.FloatField(db_column='varianceTempSer')  # Field name made lowercase.
    standarddeviationtempser = models.FloatField(db_column='standardDeviationTempSer')  # Field name made lowercase.
    mediantempser = models.FloatField(db_column='medianTempSer')  # Field name made lowercase.
    maxvaluetempser = models.FloatField(db_column='maxValueTempSer')  # Field name made lowercase.
    rmsvaluetempser = models.FloatField(db_column='rmsValueTempSer')  # Field name made lowercase.
    energytempser = models.FloatField(db_column='energyTempSer')  # Field name made lowercase.
    maxenergyintervaltempser = models.FloatField(db_column='maxEnergyIntervalTempSer')  # Field name made lowercase.
    shannonentropytempser = models.FloatField(db_column='shannonEntropyTempSer')  # Field name made lowercase.
    durationtempser = models.FloatField(db_column='durationTempSer')  # Field name made lowercase.
    wavecontrasttempser = models.FloatField(db_column='waveContrastTempSer')  # Field name made lowercase.
    wavekurtosistempser = models.FloatField(db_column='waveKurtosisTempSer')  # Field name made lowercase.
    waveskewnesstempser = models.FloatField(db_column='waveSkewnessTempSer')  # Field name made lowercase.
    envelopecontrasttempser = models.FloatField(db_column='envelopeContrastTempSer')  # Field name made lowercase.
    envelopekurtosistempser = models.FloatField(db_column='envelopeKurtosisTempSer')  # Field name made lowercase.
    envelopeskewnesstempser = models.FloatField(db_column='envelopeSkewnessTempSer')  # Field name made lowercase.
    band01envelopeenergytempser = models.FloatField(db_column='band01EnvelopeEnergyTempSer')  # Field name made lowercase.
    band02envelopeenergytempser = models.FloatField(db_column='band02EnvelopeEnergyTempSer')  # Field name made lowercase.
    band03envelopeenergytempser = models.FloatField(db_column='band03EnvelopeEnergyTempSer')  # Field name made lowercase.
    band04envelopeenergytempser = models.FloatField(db_column='band04EnvelopeEnergyTempSer')  # Field name made lowercase.
    band05envelopeenergytempser = models.FloatField(db_column='band05EnvelopeEnergyTempSer')  # Field name made lowercase.
    band01envelopekurtosistempser = models.FloatField(db_column='band01EnvelopeKurtosisTempSer')  # Field name made lowercase.
    band02envelopekurtosistempser = models.FloatField(db_column='band02EnvelopeKurtosisTempSer')  # Field name made lowercase.
    band03envelopekurtosistempser = models.FloatField(db_column='band03EnvelopeKurtosisTempSer')  # Field name made lowercase.
    band04envelopekurtosistempser = models.FloatField(db_column='band04EnvelopeKurtosisTempSer')  # Field name made lowercase.
    band05envelopekurtosistempser = models.FloatField(db_column='band05EnvelopeKurtosisTempSer')  # Field name made lowercase.
    melc1tempser = models.FloatField(db_column='melC1TempSer')  # Field name made lowercase.
    melc2tempser = models.FloatField(db_column='melC2TempSer')  # Field name made lowercase.
    melc3tempser = models.FloatField(db_column='melC3TempSer')  # Field name made lowercase.
    melc4tempser = models.FloatField(db_column='melC4TempSer')  # Field name made lowercase.
    frequencyindextempser = models.FloatField(db_column='frequencyIndexTempSer')  # Field name made lowercase.
    frequencyratiotempser = models.FloatField(db_column='frequencyRatioTempSer')  # Field name made lowercase.
    minfrequencytempser = models.FloatField(db_column='minFrequencyTempSer')  # Field name made lowercase.
    powerspectrumkurtosistempser = models.FloatField(db_column='powerSpectrumKurtosisTempSer')  # Field name made lowercase.
    powerspectrumskewnesstempser = models.FloatField(db_column='powerSpectrumSkewnessTempSer')  # Field name made lowercase.
    starttimetempser = models.DateTimeField(db_column='startTimeTempSer')  # Field name made lowercase.
    datecreationtempser = models.DateTimeField(db_column='dateCreationTempSer',auto_now_add=True)  # Field name made lowercase.
    statetempser = models.SmallIntegerField(db_column='stateTempSer')  # Field name made lowercase.

    class Meta:
        db_table = 'TemporarySeries'


class UserP(models.Model):
    #id = models.BigAutoField(primary_key=True)
    id = models.OneToOneField(User,related_name='user_profile', on_delete=models.CASCADE, primary_key=True,unique=True)
    email = models.CharField(max_length=512)
    password = models.CharField(max_length=64)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128, blank=True, null=True)
    imagecover = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=512, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=128)
    adress = models.CharField(max_length=512, blank=True, null=True)
    city = models.CharField(max_length=512, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True, default = 1)#1 activo
    datecreation = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(default = 1)# 0 admin 1 investigador 2 public


    class Meta:
        db_table = 'User'


class Volcano(models.Model):
    idvolcano = models.BigAutoField(db_column='idVolcano', primary_key=True)  # Field name made lowercase.
    shortnamevol = models.CharField(db_column='shortNameVol', max_length=20)  # Field name made lowercase.
    longnamevol = models.CharField(db_column='longNameVol', max_length=126)  # Field name made lowercase.
    descriptionvol = models.TextField(db_column='descriptionVol')  # Field name made lowercase.
    latitudevol = models.FloatField(db_column='latitudeVol')  # Field name made lowercase.
    longitudevol = models.FloatField(db_column='longitudeVol')  # Field name made lowercase.
    altitudevol = models.FloatField(db_column='altitudeVol')  # Field name made lowercase.
    pwavespeedvol = models.FloatField(db_column='pWaveSpeedVol')  # Field name made lowercase.
    densityvol = models.FloatField(db_column='densityVol')  # Field name made lowercase.
    attcorrectfactorvol = models.FloatField(db_column='attCorrectFactorVol')  # Field name made lowercase.
    indvol = models.IntegerField(db_column='indVol')  # Field name made lowercase.
    statevol = models.SmallIntegerField(db_column='stateVol')  # Field name made lowercase.
    datecreationvol = models.DateTimeField(db_column='DateCreationVol')  # Field name made lowercase.

    class Meta:
        db_table = 'Volcano'