# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
'''
    startimealert =
    idevent = 
    idimage = 
    idmask = 
    idashdirection
    idashdispersion
    idashfallprediction
    '''

class Alarm(models.Model):
    idalarm = models.CharField(db_column='idAlarm', max_length=17, primary_key=True, blank=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    alarmtype = models.CharField(db_column='alarmType', max_length=2)  # Field name made lowercase.
    sent = models.CharField(max_length=2)
    idexplosion = models.ForeignKey('Explosion', models.DO_NOTHING,db_column='idExplosion')  # Field name made lowercase.
    #idexplosion = models.CharField(db_column='idExplosion', max_length=17)  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano')  # Field name made lowercase.
    #idvolcano = models.CharField(db_column='idVolcano', max_length=3)  # Field name made lowercase.
    ind = models.CharField(max_length=2, blank=True, null=True)
    idstation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idStation', blank=True, null=True)  # Field name made lowercase.
    #idstation = models.CharField(db_column='idStation', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Alarm'



class Alert(models.Model):
    messagealert = models.TextField(db_column='messageAlert', blank = True)  # Field name made lowercase.
    idalert = models.CharField(max_length=24,db_column='idAlert', primary_key=True, blank= True) # Field name made lowercase.
    datecreationalert = models.DateTimeField(db_column='dateCreationAlert',auto_now_add=True)  # Field name made lowercase.
    statealert = models.IntegerField(db_column='stateAlert')  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano')  # Field name made lowercase.
    idalertconf = models.ForeignKey('Alertconfiguration', on_delete=models.CASCADE, db_column='idAlertConf')  # Field name made lowercase.
    #startalert = models.SmallIntegerField(db_column='startAlert', blank=True, null=True)  # Field name made lowercase.
    
    longitudealert = models.FloatField(db_column='longitudeAlert', blank=True, null=True)  # Field name made lowercase.
    latitudealert = models.FloatField(db_column='latitudeAlert', blank=True, null=True)  # Field name made lowercase.
    idashdispersion = models.ForeignKey('AshDispersion', models.DO_NOTHING, db_column='idAshDispersion', blank=True, null=True)  # Field name made lowercase.
    typealert =  models.SmallIntegerField(db_column='typeAlert')  # Field name made lowercase.

    heighalert = models.FloatField(db_column='heighAlert')  # copiar de mask
    idstation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idStation')  # Field name made lowercase.
    alertlevelalert  =models.CharField(max_length=10,db_column='alertLevelAlert')#copiar de volcan

    idimgraw = models.ForeignKey('Imagesegmentation', models.DO_NOTHING, db_column='idPhoto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Alert'
    def generate_default_idalert(self):
        now = timezone.now()
        date_time = now.strftime('%Y%m%d%H%M%S')
        VVV = self.idvolcano.shortnamevol[:3].upper() if self.idvolcano.shortnamevol else 'VVV'
        return f"{VVV}{date_time}"

    def save(self, *args, **kwargs):
        if not self.idalert:
            self.idalert = self.generate_default_idalert()
        super().save(*args, **kwargs)


class Alertconfiguration(models.Model):
    idalertconf = models.CharField(max_length=24,db_column='idAlertConf', primary_key=True, blank= True)  # Field name made lowercase.
    altitudalertconf = models.FloatField(db_column='altitudAlertConf')  # Field name made lowercase.
    statealertconf = models.IntegerField(db_column='stateAlertConf')  # Field name made lowercase.
    datecreationalertconf = models.DateTimeField(db_column='dateCreationAlertConf',auto_now_add=True)  # Field name made lowercase.
    #idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano', blank=True, null=True)  # Field name made lowercase.
    idvolcano = models.OneToOneField('Volcano', on_delete=models.CASCADE, db_column='idVolcano', related_name='alert_configuration', blank=True, null=True)
    notificationalertconf = models.BigIntegerField(db_column='notificationAlertConf', blank=True, null=True)  # Field name made lowercase.
    messagetemplateconfalert = models.TextField(db_column='messageTemplateConfAlert', blank=True, null=True)  # Field name made lowercase.
    mensajeriaalertconf = models.SmallIntegerField(db_column='mensajeriaAlertConf', blank=True, null=True)  # Field name made lowercase.
    startalert = models.SmallIntegerField(db_column='startAlertConf') 

    class Meta:
        db_table = 'AlertConfiguration'
    def generate_default_idalertconf(self):
        VVVV = self.idvolcano.shortnamevol[:4].upper() if self.idvolcano.shortnamevol else 'VVVV'
        ccc = Alertconfiguration.objects.filter(idalertconf__startswith=f"{VVVV}").count()
        return f"{VVVV}{ccc:03d}"

    def save(self, *args, **kwargs):
        if not self.idalertconf:
            self.idalertconf = self.generate_default_idalertconf()
        super().save(*args, **kwargs)


class Blob(models.Model):#SABCAJA2023082202000000
    idblob = models.CharField(max_length=24,db_column='idBlob', primary_key=True, blank=True ) # Field name made lowercase.
    idmask = models.ForeignKey('Mask', on_delete=models.CASCADE, db_column='idMask')  # Field name made lowercase.
    indblob = models.CharField(max_length=1,db_column='indblob')  # Field name made lowercase.
    perimetertblob = models.FloatField(db_column='perimeterblob')  # Field name made lowercase.
    xcentroidtblob = models.FloatField(db_column='xCentroidblob')  # Field name made lowercase.
    ycentroidtblob = models.FloatField(db_column='yCentroidblob')  # Field name made lowercase.
    areatblob = models.FloatField(db_column='areablob')  # Field name made lowercase.
    stateblob = models.SmallIntegerField(db_column='stateBlob')  # Field name made lowercase.
    datecreationblob = models.DateTimeField(db_column='dateCreationBlob',auto_now_add=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Blob'
    def generate_default_idblob(self):
        now = timezone.now()
        date_time = now.strftime('%Y%m%d%H%M%S')
        VVV = self.idmask.idmask.idstation.idvolcano.shortnamevol[:3].upper() if self.idmask.idmask.idstation.idvolcano.shortnamevol else 'VVV'
        SSSS = self.idmask.idmask.idstation.shortnamestat[:4].upper() if self.idmask.idmask.idstation.shortnamestat else 'SSSS'
        ccc = Blob.objects.filter(idblob__startswith=f"{VVV}{SSSS}{date_time}").count()
        return f"{VVV}{SSSS}{date_time}{ccc:03d}"

    def save(self, *args, **kwargs):
        if not self.idblob:
            self.idblob = self.generate_default_idblob()
        super().save(*args, **kwargs)

class Eventtype(models.Model):
    ideventtype = models.CharField(max_length=3,db_column='idEventType', primary_key=True) 
    nameevent = models.CharField(db_column='nameEvent', max_length=126)  # Field name made lowercase.
    datecreationevent = models.DateTimeField(db_column='dateCreationEvent',auto_now_add=True)  # Field name made lowercase.
    stateevent = models.SmallIntegerField(db_column='stateEvent')  # Field name made lowercase.

    class Meta:
        db_table = 'EventType'

    def generate_default_ideventtype(self):
        NN = self.nameevent[:1] if self.nameevent else 'N'
        return f"{NN}"

    def save(self, *args, **kwargs):
        if not self.ideventtype:
            self.ideventtype = self.generate_default_ideventtype()
        super().save(*args, **kwargs)


class Explosion(models.Model):
    idexplosion = models.CharField(db_column='idExplosion', max_length=17, primary_key=True, blank=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    ideventtype = models.ForeignKey(Eventtype, models.DO_NOTHING,db_column='idEvent', blank=True, null=True)  # Field name made lowercase.
    #idevent = models.CharField(db_column='idEvent', max_length=21)  # Field name made lowercase.
    idimage = models.ForeignKey('Imagesegmentation', models.DO_NOTHING, db_column='idImage', blank=True, null=True)  # Field name made lowercase.
    #idimage = models.CharField(db_column='idImage', max_length=21, blank=True, null=True)  # Field name made lowercase.
    #idmask = models.ForeignKey('Mask', on_delete=models.DO_NOTHING, db_column='idMask', blank=True, null=True)  # Field name made lowercase.
    #idmask = models.CharField(db_column='idMask', max_length=21, blank=True, null=True)  # Field name made lowercase.
    height = models.FloatField(blank=True, null=True)
    #ashdirection = models.ForeignKey('Ashfallprediction', models.DO_NOTHING,db_column='ashDirection', blank=True, null=True)  # Field name made lowercase.
    ashdirection = models.CharField(db_column='ashDirection', max_length=30, blank=True, null=True)  # Field name made lowercase.
    #idwinddir = models.ForeignKey(db_column='idWinddir', max_length=19, blank=True, null=True)  # Field name made lowercase.
    idwinddir = models.ForeignKey('Winddirection', models.DO_NOTHING,db_column='idWinddir', max_length=19, blank=True, null=True)  # Field name made lowercase.

    idashdispersion = models.ForeignKey('Ashdispersion', models.DO_NOTHING, db_column='idAshDispersion', max_length=17, blank=True, null=True)  # Field name made lowercase.
    #ashdirection = models.ForeignKey('Ashfallprediction', models.DO_NOTHING,db_column='ashDirection', blank=True, null=True)  # Field name made lowercase.
    idashfallprediction = models.ForeignKey('Ashfallprediction', models.DO_NOTHING, blank=True, null=True,db_column='idAshfallprediction')  # Field name made lowercase.
    detectionmode = models.CharField(db_column='detectionMode', max_length=2)  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano')  # Field name made lowercase.
    #idvolcano = models.CharField(db_column='idVolcano', max_length=3)  # Field name made lowercase.
    ind = models.CharField(max_length=2, blank=True, null=True)
    #idstation = models.CharField(db_column='idStation', max_length=4)  # Field name made lowercase.
    idstation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idStation', blank=True, null=True)  # Field name made lowercase.
    data = models.JSONField(blank=True, null=True)
    class Meta:
        db_table = 'Explosion'

class History(models.Model):
    idhistory = models.BigAutoField(db_column='idHistory', primary_key=True)  # Field name made lowercase.
    datemodificationhistory = models.DateTimeField(db_column='dateModificationHistory')  # Field name made lowercase.
    contentstringhistory = models.TextField(db_column='contentStringHistory')  # Field name made lowercase.
    statepermissionchangehistory = models.IntegerField(db_column='statePermissionChangeHistory')  # Field name made lowercase.
    datepermissionchangehistory = models.TimeField(db_column='datePermissionChangeHistory')  # Field name made lowercase.
    idtabletochangehistory = models.BigIntegerField(db_column='idTableToChangeHistory')  # Field name made lowercase.
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='idUser')  # Field name made lowercase.
    idregisterhistory = models.BigIntegerField(db_column='idRegisterHistory')  # Field name made lowercase.
    statehistory = models.SmallIntegerField(db_column='stateHistory')  # Field name made lowercase.

    class Meta:
        db_table = 'History'


class Imagesegmentation(models.Model):
    idphoto = models.CharField(max_length=21, db_column='idPhoto', primary_key=True, blank=True)  # Field name made lowercase.
    urlimg = models.TextField(db_column='urlImg')  # Field name made lowercase.
    filenameimg = models.CharField(db_column='fileNameImg', max_length=128)  # Field name made lowercase.
    stateimg = models.SmallIntegerField(db_column='stateImg', null=False)  # Field name made lowercase.
    datecreationimg = models.DateTimeField(db_column='dateCreationImg',auto_now_add=True)  # Field name made lowercase.
    idstation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idStation')  # Field name made lowercase.

    class Meta:
        db_table = 'ImageSegmentation'
    
    def generate_default_idIS(self):
        #date_time =  self.datecreationimg.strftime('%Y%m%d%H%M%S')
        date_time = timezone.now().strftime('%Y%m%d%H%M%S')
        VVV = self.idstation.idvolcano.shortnamevol[:3].upper() if self.idstation.idvolcano.shortnamevol else 'VVV'
        SSSS = self.idstation.shortnamestat[:4].upper() if self.idstation.shortnamestat else 'SSSS'
        return f"{VVV}{SSSS}{date_time}"

    def save(self, *args, **kwargs):
        if not self.idphoto:
            self.idphoto = self.generate_default_idIS()
        super().save(*args, **kwargs)


class Mask(models.Model):#SABCAJA20230822020000
    idmask = models.OneToOneField(Imagesegmentation,db_column='idMask', primary_key=True,on_delete=models.CASCADE)  # Field name made lowercase.
    indmask = models.SmallIntegerField(db_column='indmask')  # Field name made lowercase.
    starttimemask = models.DateTimeField(db_column='startTimemask')  # Field name made lowercase.
    filenamemask = models.TextField(db_column='fileNamemask')  # Field name made lowercase.
    directionmask = models.TextField(db_column='directionmask')  # Field name made lowercase.
    heighmask = models.FloatField(db_column='heighmask')  # Field name made lowercase.
    statemask = models.SmallIntegerField(db_column='statemask', null=False)  # Field name made lowercase.
    idstation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idStation')  # Field name made lowercase.

    class Meta:
        db_table = 'Mask'
#no tiene auto generador de id porque su id es un imageraw

class Winddirection(models.Model):
    starttimewinddir = models.DateTimeField(db_column='startTimeWinddir')  # Field name made lowercase.
    latitudewinddir = models.FloatField(db_column='latitudeWinddir')  # Field name made lowercase.
    longitudewinddir = models.FloatField(db_column='longitudeWinddir')  # Field name made lowercase.
    uwinddir = models.FloatField(db_column='uWinddir')  # Field name made lowercase.
    vwinddir = models.FloatField(db_column='vWinddir')  # Field name made lowercase.
    speedwinddir = models.FloatField(db_column='speedWinddir')  # Field name made lowercase.
    directionwinddir = models.FloatField(db_column='directionWinddir')  # Field name made lowercase.
    temperaturewinddir = models.FloatField(db_column='temperatureWinddir')  # Field name made lowercase.
    geopotentialheightwinddir = models.FloatField(db_column='geopotentialHeightWinddir')  # Field name made lowercase.
    indwinddir = models.IntegerField(db_column='indWinddir', blank=True, null=True)  # Field name made lowercase.
    #jsonwinddir = models.JSONField(db_column='jsonWinddir',)  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano', blank=True, null=True)  # Field name made lowercase.
    #idwtation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idStation')  # Field name made lowercase.
    #idtemporarwseries = models.ForeignKey('Temporaryseries', models.DO_NOTHING, db_column='idTemporarySeries', blank=True, null=True)  # Field name made lowercase.                                                        5                                                                                                                                                                                                                                              w       = models.ForeignKey('Temporaryseries', models.DO_NOTHING, db_column='idTemporarySeries', blank=True, null=True)  # Field name made lowercase.
    statewinddir = models.SmallIntegerField(db_column='stateWinddir',default= 1)  # Field name made lowercase.
    idwinddirection = models.CharField(max_length=21,db_column='idWinddir', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'WindDirection'

    def generate_default_idWD(self):
        now = timezone.now()
        date_time = now.strftime('%Y%m%d%H%M%S')
        VVV = self.idvolcano.shortnamevol[:3].upper() if self.idvolcano.shortnamevol else 'VVV'
        cc = Winddirection.objects.filter(idwinddirection__startswith=f"{VVV}{date_time}").count()
        return f"{VVV}{date_time}{cc:02d}"
    
    def save(self, *args, **kwargs):
        if not self.idwinddirection:
            self.idphoto = self.generate_default_idWD()
        super().save(*args, **kwargs)

class Ashfallprediction(models.Model):
    idashfallprediction = models.CharField(max_length=21,db_column='idAshfallprediction', primary_key=True)  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano', blank=True, null=True)  # Field name made lowercase.
    typeashfall = models.CharField(max_length=3,db_column='typeAshfall') 

    jsonbodyashfall = models.JSONField(db_column='jsonbodyAshfall',)  # Field name made lowercase.
    #bodyashfall =
    starttimeashfall = models.DateTimeField(db_column='startTimeAshfall')  # Field name made lowercase.
    stateashfall = models.SmallIntegerField(db_column='stateAshfall',default= 1)  # Field name made lowercase.

    class Meta:
        db_table = 'AshFallPrediction'

    def generate_default_idAFD(self):
        now = timezone.now()
        date_time = now.strftime('%Y%m%d%H%M%S')
        VVV = self.idvolcano.shortnamevol[:3].upper() if self.idvolcano.shortnamevol else 'VVV'
        return f"{VVV}{date_time}"
    
    def save(self, *args, **kwargs):
        if not self.idashfallprediction:
            self.idphoto = self.generate_default_idAFD()
        super().save(*args, **kwargs)


class Ashdispersion(models.Model):
    OPCIONES = [
        ('OBSERVED', ''),
        ('FORECAST', ''),
    ]
    idashdispersion = models.CharField(max_length=21,db_column='idAshDispersion', primary_key=True)  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano', blank=True, null=True)  # Field name made lowercase.
    jsonashdisp = models.JSONField(db_column='jsonAshdisp',)  # Field name made lowercase.
    starttimeashdisp = models.DateTimeField(db_column='startTimeAshdisp')  # Field name made lowercase.
    urlfileashdisp = models.TextField(db_column='urlfileAshdisp')  # Field name made lowercase.
    idnoticeashdisp  = models.CharField(max_length=10,db_column='idNoticeAshdisp')  # Field name made lowercase.
    idtypeashdisp  =models.CharField(max_length=10, choices=OPCIONES,db_column='idTypeAshdisp')
    stateashdisp = models.SmallIntegerField(db_column='stateAshdisp',default= 1)  # Field name made lowercase.

    class Meta:
        db_table = 'AshDispersion'

    def generate_default_idAD(self):
        now = timezone.now()
        date_time = now.strftime('%Y%m%d%H%M%S')
        VVV = self.idvolcano.shortnamevol[:3].upper() if self.idvolcano.shortnamevol else 'VVV'
        return f"{VVV}{date_time}"
    
    def save(self, *args, **kwargs):
        if not self.idashdispersion:
            self.idphoto = self.generate_default_idAD()
        super().save(*args, **kwargs)

class Station(models.Model):
    idstation = models.CharField(db_column='idStation', max_length=5, primary_key=True, blank = True)  # Field name made lowercase.
    standardnamestat = models.CharField(db_column='standardNameStat', max_length=64)  # Field name made lowercase.
    shortnamestat = models.CharField(db_column='shortNameStat', max_length=20)  # Field name made lowercase.
    longnamestat = models.CharField(db_column='longNameStat', max_length=126)  # Field name made lowercase.
    latitudestat = models.FloatField(db_column='latitudeStat')  # Field name made lowercase.
    longitudestat = models.FloatField(db_column='longitudeStat')  # Field name made lowercase.
    altitudestat = models.FloatField(db_column='altitudeStat')  # Field name made lowercase.
    indstat = models.IntegerField(db_column='indStat')  # Field name made lowercase.
    statestat = models.IntegerField(db_column='stateStat')  # Field name made lowercase.
    datecreationstat = models.DateTimeField(db_column='dateCreationStat',auto_now_add=True)  # Field name made lowercase.
    typestat = models.SmallIntegerField(db_column='typeStat', blank=True, null=True)  # Field name made lowercase.
    idvolcano = models.ForeignKey('Volcano', models.DO_NOTHING, db_column='idVolcano')  # Field name made lowercase.

    class Meta:
        db_table = 'Station'
    def generate_default_idstation(self):
        N = self.shortnamestat[:4].upper() if self.shortnamestat else 'NNNN'
        return N

    def save(self, *args, **kwargs):
        if not self.idstation:
            self.idstation = self.generate_default_idstation()
        super().save(*args, **kwargs)

class Temporaryseries(models.Model): #SABSABA20230820202649
    idtemporaryseries  = models.CharField(max_length=21, primary_key=True, db_column='idTemporarySeries', blank=True)
    idstation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idStation')  # Field name made lowercase.
    ideventtype = models.ForeignKey(Eventtype, models.DO_NOTHING,db_column='idEventType', max_length=3, blank=True, null=True)  # Field name made lowercase.
    durationtempser = models.FloatField(db_column='durationTempSer')  # Field name made lowercase.
    energytempser = models.FloatField(db_column='energyTempSer')  # Field name made lowercase.
    freqindextempser = models.FloatField(db_column='freqIndexTempSer')  # Field name made lowercase.
    attackratiotempser = models.FloatField(db_column='attackRatioTempSer')  # Field name made lowercase.
    decayratiotempser = models.FloatField(db_column='decayRatioTempSer')  # Field name made lowercase.
    meantempser = models.FloatField(db_column='meanTempSer')  # Field name made lowercase.
    standarddeviationtempser = models.FloatField(db_column='standardDeviationTempSer')  # Field name made lowercase.
    skewnesstempser = models.FloatField(db_column='skewnessTempSer')  # Field name made lowercase.
    kurtosistempser = models.FloatField(db_column='kurtosisTempSer')  # Field name made lowercase.
    centralenergytempser = models.FloatField(db_column='centralEnergyTempSer')  # Field name made lowercase.
    rmsbandwidthtempser = models.FloatField(db_column='rmsBandwidthTempSer')  # Field name made lowercase.
    meanskewnesstempser = models.FloatField(db_column='meanSkewnessTempSer')  # Field name made lowercase.
    meankurtosistempser = models.FloatField(db_column='meanKurtosisTempSer')  # Field name made lowercase.
    entropytempser = models.FloatField(db_column='entropyTempSer')  # Field name made lowercase.
    brightnesstempser = models.FloatField(db_column='brightnessTempSer')  # Field name made lowercase.
    shannonentropytempser = models.FloatField(db_column='shannonEntropyTempSer')  # Field name made lowercase.
    renyientropytempser = models.FloatField(db_column='renyiEntropyTempSer')  # Field name made lowercase.
    lpc1tempser = models.FloatField(db_column='lpc1TempSer')  # Field name made lowercase.
    lpc2tempser = models.FloatField(db_column='lpc2TempSer')  # Field name made lowercase.
    lpc3tempser = models.FloatField(db_column='lpc3TempSer')  # Field name made lowercase.
    lpc4tempser = models.FloatField(db_column='lpc4TempSer')  # Field name made lowercase.
    lpc5tempser = models.FloatField(db_column='lpc5TempSer')  # Field name made lowercase.
    cc1tempser = models.FloatField(db_column='cc1TempSer')  # Field name made lowercase.
    cc2tempser = models.FloatField(db_column='cc2TempSer')  # Field name made lowercase.
    cc3tempser = models.FloatField(db_column='cc3TempSer')  # Field name made lowercase.
    cc4tempser = models.FloatField(db_column='cc4TempSer')  # Field name made lowercase.
    cc5tempser = models.FloatField(db_column='cc5TempSer')  # Field name made lowercase.
    starttimetempser = models.DateTimeField(db_column='startTimeTempSer')  # Field name made lowercase.
    datecreationtempser = models.DateTimeField(db_column='dateCreationTempSer')  # Field name made lowercase.
    statetempser = models.SmallIntegerField(db_column='stateTempSer')  # Field name made lowercase.
    indtempser = models.IntegerField(db_column='indTempSer', blank=True, null=True)  # Field name made lowercase.
    relativeheight = models.CharField(db_column='relativeHeight', blank=True, null=True)  # Field name made lowercase.

    def generate_default_idtemporaryseries(self):
        now = timezone.now()
        date_time = now.strftime('%Y%m%d%H%M%S')
        VVV = self.idstation.idvolcano.shortnamevol[:3].upper() if self.idstation.idvolcano.shortnamevol else 'VVV'
        SSSS = self.idstation.shortnamestat[:4].upper() if self.idstation.shortnamestat else 'SSSS'
        return f"{VVV}{SSSS}{date_time}"

    def save(self, *args, **kwargs):
        if not self.idtemporaryseries:
            self.idtemporaryseries = self.generate_default_idtemporaryseries()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'TemporarySeries'

    


class UserP(models.Model):
    #id = models.BigAutoField(primary_key=True)
    id = models.OneToOneField(User,related_name='user_profile', on_delete=models.CASCADE, primary_key=True,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=64)
    #firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128, blank=True, null=True)
    imagecover = models.ImageField( blank=True)
    imageprofile = models.ImageField( blank=True)
    country = models.CharField(max_length=512, blank=True, null=True)
    comment = models.CharField(max_length=8192)
    phone = models.CharField(max_length=12, unique=True)
    names = models.CharField(max_length=128)
    institution = models.CharField(max_length=512)
    city = models.CharField(max_length=512, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True, default = 1)#1 activo
    datecreation = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(default = 3)# 0 admin 1 investigador 2 public 3 en espera


    class Meta:
        db_table = 'User'
    def __str__(self):
        return self.email
    
class Volcano(models.Model):
    OPCIONES = [
        ('Medio', ''),
        ('Bajo', ''),
        ('Alto', ''),
    ]
    shortnamevol = models.CharField(db_column='shortNameVol', max_length=20)  # Field name made lowercase.
    longnamevol = models.CharField(db_column='longNameVol', max_length=126)  # Field name made lowercase.
    idvolcano = models.CharField(db_column='idVolcano', max_length=9, primary_key=True,
        blank=True,  # Permite que idvolcano no sea obligatorio
    )
    descriptionvol = models.TextField(db_column='descriptionVol')  # Field name made lowercase.
    latitudevol = models.FloatField(db_column='latitudeVol')  # Field name made lowercase.
    longitudevol = models.FloatField(db_column='longitudeVol')  # Field name made lowercase.
    altitudevol = models.FloatField(db_column='altitudeVol')  # Field name made lowercase.
    pwavespeedvol = models.FloatField(db_column='pWaveSpeedVol')  # Field name made lowercase.
    densityvol = models.FloatField(db_column='densityVol')  # Field name made lowercase.
    attcorrectfactorvol = models.FloatField(db_column='attCorrectFactorVol')  # Field name made lowercase.
    indvol = models.IntegerField(db_column='indVol')  # Field name made lowercase.
    statevol = models.SmallIntegerField(db_column='stateVol')  # Field name made lowercase.
    datecreationvol = models.DateTimeField(auto_now_add=True,db_column='DateCreationVol')  # Field name made lowercase.
    alertlevelvol  =models.CharField(max_length=10, choices=OPCIONES,db_column='alertLevelVol')

    class Meta:
        db_table = 'Volcano'
    
    def generate_default_idvolcano(self):
        VVV = self.shortnamevol[:3].upper() if self.shortnamevol else 'VVV'
        #count = Volcano.objects.filter(idvolcano__startswith=VVV).count() + 1
        return f"{VVV}"

    def save(self, *args, **kwargs):
        if not self.idvolcano:
            self.idvolcano = self.generate_default_idvolcano()
        super().save(*args, **kwargs)

class Mapping(models.Model):
    tablenamemap = models.CharField(max_length=50, db_column='tablenameMap', primary_key=True)
    attributeskeysmap = models.JSONField(db_column='attributeskeysMap')  # Field name made lowercase.
