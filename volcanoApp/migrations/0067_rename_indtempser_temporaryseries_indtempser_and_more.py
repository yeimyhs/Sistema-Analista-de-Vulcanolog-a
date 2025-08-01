# Generated by Django 4.2.7 on 2024-02-07 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('volcanoApp', '0066_alter_station_idvolcano'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temporaryseries',
            old_name='indtempser',
            new_name='indTempSer',
        ),
        migrations.RenameField(
            model_name='temporaryseries',
            old_name='meantempser',
            new_name='meanTempSer',
        ),
        migrations.RenameField(
            model_name='temporaryseries',
            old_name='shannonentropytempser',
            new_name='shannonEntropyTempSer',
        ),
        migrations.RenameField(
            model_name='temporaryseries',
            old_name='standarddeviationtempser',
            new_name='standardDeviationTempSer',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band01envelopeenergytempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band01envelopekurtosistempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band02envelopeenergytempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band02envelopekurtosistempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band03envelopeenergytempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band03envelopekurtosistempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band04envelopeenergytempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band04envelopekurtosistempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band05envelopeenergytempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='band05envelopekurtosistempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='durationtempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='energytempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='envelopecontrasttempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='envelopekurtosistempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='envelopeskewnesstempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='frequencyindextempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='frequencyratiotempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='maxenergyintervaltempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='maxvaluetempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='mediantempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='melc1tempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='melc2tempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='melc3tempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='melc4tempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='minfrequencytempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='powerspectrumkurtosistempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='powerspectrumskewnesstempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='rmsvaluetempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='variancetempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='wavecontrasttempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='wavekurtosistempser',
        ),
        migrations.RemoveField(
            model_name='temporaryseries',
            name='waveskewnesstempser',
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='brightnessTempSer',
            field=models.FloatField(db_column='brightnessTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='cc1TempSer',
            field=models.FloatField(db_column='cc1TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='cc2TempSer',
            field=models.FloatField(db_column='cc2TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='cc3TempSer',
            field=models.FloatField(db_column='cc3TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='cc4TempSer',
            field=models.FloatField(db_column='cc4TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='cc5TempSer',
            field=models.FloatField(db_column='cc5TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='centralEnergyTempSer',
            field=models.FloatField(db_column='centralEnergyTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='entropyTempSer',
            field=models.FloatField(db_column='entropyTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='kurtosisTempSer',
            field=models.FloatField(db_column='kurtosisTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='lpc1TempSer',
            field=models.FloatField(db_column='lpc1TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='lpc2TempSer',
            field=models.FloatField(db_column='lpc2TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='lpc3TempSer',
            field=models.FloatField(db_column='lpc3TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='lpc4TempSer',
            field=models.FloatField(db_column='lpc4TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='lpc5TempSer',
            field=models.FloatField(db_column='lpc5TempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='meanKurtosisTempSer',
            field=models.FloatField(db_column='meanKurtosisTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='meanSkewnessTempSer',
            field=models.FloatField(db_column='meanSkewnessTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='relativeHeight',
            field=models.FloatField(blank=True, db_column='relativeHeight', null=True),
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='renyiEntropyTempSer',
            field=models.FloatField(db_column='renyiEntropyTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='rmsBandwidthTempSer',
            field=models.FloatField(db_column='rmsBandwidthTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryseries',
            name='skewnessTempSer',
            field=models.FloatField(db_column='skewnessTempSer', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='temporaryseries',
            name='ideventtype',
            field=models.ForeignKey(db_column='idEventType', default='NOC', on_delete=django.db.models.deletion.CASCADE, to='volcanoApp.eventtype'),
        ),
    ]
