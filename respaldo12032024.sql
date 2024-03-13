--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5 (Debian 15.5-0+deb12u1)
-- Dumped by pg_dump version 15.5 (Debian 15.5-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Alarm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Alarm" (
    "idAlarm" character varying(17) NOT NULL,
    "startTime" timestamp without time zone NOT NULL,
    "alarmType" character varying(2) NOT NULL,
    sent character varying(2) NOT NULL,
    "idExplosion" character varying(17) NOT NULL,
    "idVolcano" character varying(3) NOT NULL,
    ind character varying(2),
    "idStation" character varying(4)
);


ALTER TABLE public."Alarm" OWNER TO postgres;

--
-- Name: Alert; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Alert" (
    "messageAlert" text NOT NULL,
    "idAlert" character varying(24) NOT NULL,
    "stateAlert" integer NOT NULL,
    "idVolcano" character varying(9) NOT NULL,
    "idAlertConf" character varying(24) NOT NULL,
    "startAlert" smallint,
    "dateCreationAlert" timestamp with time zone NOT NULL,
    "alertLevelAlert" character varying(10) NOT NULL,
    "heighAlert" double precision NOT NULL,
    "idStation" character varying(5) NOT NULL,
    "idAshDispersion" character varying(21),
    "latitudeAlert" double precision,
    "longitudeAlert" double precision,
    "typeAlert" smallint NOT NULL,
    "idPhoto" character varying(21) NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."Alert" OWNER TO postgres;

--
-- Name: AlertConfiguration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."AlertConfiguration" (
    "idAlertConf" character varying(24) NOT NULL,
    "altitudAlertConf" double precision NOT NULL,
    "stateAlertConf" integer NOT NULL,
    "idVolcano" character varying(9),
    "notificationAlertConf" bigint,
    "messageTemplateConfAlert" text,
    "mensajeriaAlertConf" smallint,
    "startAlertConf" smallint NOT NULL,
    "dateCreationAlertConf" timestamp with time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."AlertConfiguration" OWNER TO postgres;

--
-- Name: AshDispersion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."AshDispersion" (
    "idAshDispersion" character varying(21) NOT NULL,
    "jsonAshdisp" jsonb NOT NULL,
    "startTimeAshdisp" timestamp without time zone NOT NULL,
    "urlfileAshdisp" text NOT NULL,
    "idNoticeAshdisp" character varying(10) NOT NULL,
    "idTypeAshdisp" character varying(10) NOT NULL,
    "idVolcano" character varying(9),
    "stateAshdisp" smallint
);


ALTER TABLE public."AshDispersion" OWNER TO postgres;

--
-- Name: AshFallPrediction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."AshFallPrediction" (
    "idAshfallprediction" character varying(21) NOT NULL,
    "startTimeAshfall" timestamp without time zone NOT NULL,
    "stateAshfall" smallint,
    "idVolcano" character varying(9) NOT NULL,
    "jsonbodyAshfall" jsonb NOT NULL,
    "typeAshfall" character varying(3) NOT NULL
);


ALTER TABLE public."AshFallPrediction" OWNER TO postgres;

--
-- Name: Blob; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Blob" (
    "idBlob" character varying(24) NOT NULL,
    "idMask" character varying(21) NOT NULL,
    "stateBlob" smallint,
    "dateCreationBlob" timestamp without time zone NOT NULL,
    areablob double precision NOT NULL,
    indblob character varying(1),
    perimeterblob double precision NOT NULL,
    "xCentroidblob" double precision NOT NULL,
    "yCentroidblob" double precision NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."Blob" OWNER TO postgres;

--
-- Name: EventType; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EventType" (
    "idEventType" character varying(3) NOT NULL,
    "nameEvent" character varying(126) NOT NULL,
    "dateCreationEvent" timestamp with time zone NOT NULL,
    "stateEvent" smallint NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."EventType" OWNER TO postgres;

--
-- Name: Explosion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Explosion" (
    "idExplosion" character varying(17) NOT NULL,
    "startTime" timestamp without time zone NOT NULL,
    "idEvent" character varying(21) NOT NULL,
    "idImage" character varying(21),
    height double precision,
    "ashDirection" character varying(30),
    "idWinddir" character varying(19),
    "idAshDispersion" character varying(17),
    "idAshfallprediction" character varying(20),
    "detectionMode" character varying(2) NOT NULL,
    "idVolcano" character varying(3) NOT NULL,
    ind character varying(2),
    "idStation" character varying(5),
    data jsonb
);


ALTER TABLE public."Explosion" OWNER TO postgres;

--
-- Name: History; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."History" (
    "idHistory" bigint NOT NULL,
    "dateModificationHistory" timestamp with time zone NOT NULL,
    "contentStringHistory" text NOT NULL,
    "statePermissionChangeHistory" integer NOT NULL,
    "datePermissionChangeHistory" time with time zone NOT NULL,
    "idTableToChangeHistory" bigint NOT NULL,
    "idUser" bigint NOT NULL,
    "idRegisterHistory" bigint NOT NULL,
    "stateHistory" smallint NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."History" OWNER TO postgres;

--
-- Name: History_idHistory_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."History_idHistory_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."History_idHistory_seq" OWNER TO postgres;

--
-- Name: History_idHistory_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."History_idHistory_seq" OWNED BY public."History"."idHistory";


--
-- Name: ImageSegmentation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ImageSegmentation" (
    "idPhoto" character varying(21) NOT NULL,
    "urlImg" text NOT NULL,
    "fileNameImg" character varying(128) NOT NULL,
    "stateImg" smallint,
    "dateCreationImg" timestamp without time zone NOT NULL,
    "idStation" character varying(5) NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."ImageSegmentation" OWNER TO postgres;

--
-- Name: Mask; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Mask" (
    "idMask" character varying(21) NOT NULL,
    directionmask text NOT NULL,
    "fileNamemask" text NOT NULL,
    heighmask double precision NOT NULL,
    "startTimemask" timestamp(6) without time zone NOT NULL,
    indmask smallint,
    statemask smallint,
    "idStation" character varying(5) NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."Mask" OWNER TO postgres;

--
-- Name: Station; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Station" (
    "idStation" character varying(5) NOT NULL,
    "standardNameStat" character varying(64) NOT NULL,
    "shortNameStat" character varying(20) NOT NULL,
    "longNameStat" character varying(126) NOT NULL,
    "latitudeStat" double precision NOT NULL,
    "longitudeStat" double precision NOT NULL,
    "altitudeStat" double precision NOT NULL,
    "indStat" integer NOT NULL,
    "stateStat" integer NOT NULL,
    "dateCreationStat" timestamp with time zone NOT NULL,
    "typeStat" smallint,
    "idVolcano" character varying(9) NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."Station" OWNER TO postgres;

--
-- Name: TemporarySeries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."TemporarySeries" (
    "idTemporarySeries" character varying(21) NOT NULL,
    "idStation" character varying(5) NOT NULL,
    "idEventType" character varying(3) DEFAULT 'NOC'::character varying,
    "durationTempSer" double precision NOT NULL,
    "energyTempSer" double precision NOT NULL,
    "freqIndexTempSer" double precision NOT NULL,
    "attackRatioTempSer" double precision NOT NULL,
    "decayRatioTempSer" double precision NOT NULL,
    "meanTempSer" double precision NOT NULL,
    "standardDeviationTempSer" double precision NOT NULL,
    "skewnessTempSer" double precision NOT NULL,
    "kurtosisTempSer" double precision NOT NULL,
    "centralEnergyTempSer" double precision NOT NULL,
    "rmsBandwidthTempSer" double precision NOT NULL,
    "meanSkewnessTempSer" double precision NOT NULL,
    "meanKurtosisTempSer" double precision NOT NULL,
    "entropyTempSer" double precision NOT NULL,
    "brightnessTempSer" double precision NOT NULL,
    "shannonEntropyTempSer" double precision NOT NULL,
    "renyiEntropyTempSer" double precision NOT NULL,
    "lpc1TempSer" double precision NOT NULL,
    "lpc2TempSer" double precision NOT NULL,
    "lpc3TempSer" double precision NOT NULL,
    "lpc4TempSer" double precision NOT NULL,
    "lpc5TempSer" double precision NOT NULL,
    "cc1TempSer" double precision NOT NULL,
    "cc2TempSer" double precision NOT NULL,
    "cc3TempSer" double precision NOT NULL,
    "cc4TempSer" double precision NOT NULL,
    "cc5TempSer" double precision NOT NULL,
    "startTimeTempSer" timestamp(6) without time zone NOT NULL,
    "dateCreationTempSer" timestamp(6) without time zone NOT NULL,
    "stateTempSer" smallint NOT NULL,
    "indTempSer" integer,
    "relativeHeight" character varying
);


ALTER TABLE public."TemporarySeries" OWNER TO postgres;

--
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User" (
    id_id integer NOT NULL,
    email character varying(254) NOT NULL,
    password character varying(64) NOT NULL,
    names character varying(128) NOT NULL,
    lastname character varying(128),
    country character varying(512),
    city character varying(512),
    state integer,
    datecreation timestamp with time zone NOT NULL,
    type integer NOT NULL,
    comment character varying(8192) NOT NULL,
    institution character varying(512) NOT NULL,
    imagecover character varying(100) NOT NULL,
    phone character varying(12) NOT NULL,
    imageprofile character varying(100) NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."User" OWNER TO postgres;

--
-- Name: Volcano; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Volcano" (
    "idVolcano" character varying(9) NOT NULL,
    "shortNameVol" character varying(20) NOT NULL,
    "longNameVol" character varying(126) NOT NULL,
    "descriptionVol" text NOT NULL,
    "latitudeVol" double precision NOT NULL,
    "longitudeVol" double precision NOT NULL,
    "altitudeVol" double precision NOT NULL,
    "pWaveSpeedVol" double precision NOT NULL,
    "densityVol" double precision NOT NULL,
    "attCorrectFactorVol" double precision NOT NULL,
    "indVol" integer NOT NULL,
    "stateVol" smallint NOT NULL,
    "DateCreationVol" timestamp with time zone NOT NULL,
    "alertLevelVol" character varying(10) NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public."Volcano" OWNER TO postgres;

--
-- Name: WindDirection; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."WindDirection" (
    "startTimeWinddir" timestamp without time zone NOT NULL,
    "latitudeWinddir" double precision NOT NULL,
    "longitudeWinddir" double precision NOT NULL,
    "uWinddir" double precision NOT NULL,
    "vWinddir" double precision NOT NULL,
    "speedWinddir" double precision NOT NULL,
    "directionWinddir" double precision NOT NULL,
    "temperatureWinddir" double precision NOT NULL,
    "geopotentialHeightWinddir" double precision NOT NULL,
    "indWinddir" integer,
    "stateWinddir" smallint,
    "idWinddir" character varying(21) NOT NULL,
    "idVolcano" character varying(9)
);


ALTER TABLE public."WindDirection" OWNER TO postgres;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: knox_authtoken; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.knox_authtoken (
    digest character varying(128) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    expiry timestamp with time zone,
    token_key character varying(8) NOT NULL
);


ALTER TABLE public.knox_authtoken OWNER TO postgres;

--
-- Name: volcanoApp_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."volcanoApp_mapping" (
    "tablenameMap" character varying(50) NOT NULL,
    "attributeskeysMap" jsonb NOT NULL
);


ALTER TABLE public."volcanoApp_mapping" OWNER TO postgres;

--
-- Name: History idHistory; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."History" ALTER COLUMN "idHistory" SET DEFAULT nextval('public."History_idHistory_seq"'::regclass);


--
-- Name: AlertConfiguration AlertConfiguration_idVolcano_049feca2_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AlertConfiguration"
    ADD CONSTRAINT "AlertConfiguration_idVolcano_049feca2_uniq" UNIQUE ("idVolcano");


--
-- Name: AshDispersion AshDispersion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AshDispersion"
    ADD CONSTRAINT "AshDispersion_pkey" PRIMARY KEY ("idAshDispersion");


--
-- Name: AshFallPrediction AshFallPrediction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AshFallPrediction"
    ADD CONSTRAINT "AshFallPrediction_pkey" PRIMARY KEY ("idAshfallprediction");


--
-- Name: Alert PK_Alert; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Alert"
    ADD CONSTRAINT "PK_Alert" PRIMARY KEY ("idAlert");


--
-- Name: AlertConfiguration PK_AlertConfiguration; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AlertConfiguration"
    ADD CONSTRAINT "PK_AlertConfiguration" PRIMARY KEY ("idAlertConf");


--
-- Name: Blob PK_Blob; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Blob"
    ADD CONSTRAINT "PK_Blob" PRIMARY KEY ("idBlob");


--
-- Name: EventType PK_EventType; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventType"
    ADD CONSTRAINT "PK_EventType" PRIMARY KEY ("idEventType");


--
-- Name: History PK_History; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."History"
    ADD CONSTRAINT "PK_History" PRIMARY KEY ("idHistory");


--
-- Name: ImageSegmentation PK_ImageSegmentation; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ImageSegmentation"
    ADD CONSTRAINT "PK_ImageSegmentation" PRIMARY KEY ("idPhoto");


--
-- Name: Mask PK_Mask; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Mask"
    ADD CONSTRAINT "PK_Mask" PRIMARY KEY ("idMask");


--
-- Name: Station PK_Station; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Station"
    ADD CONSTRAINT "PK_Station" PRIMARY KEY ("idStation");


--
-- Name: User PK_User; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "PK_User" PRIMARY KEY (id_id);


--
-- Name: Volcano PK_Volcano; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Volcano"
    ADD CONSTRAINT "PK_Volcano" PRIMARY KEY ("idVolcano");


--
-- Name: User User_email_667201b5_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_email_667201b5_uniq" UNIQUE (email);


--
-- Name: User User_phone_46f113c5_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_phone_46f113c5_uniq" UNIQUE (phone);


--
-- Name: WindDirection WindDirection_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."WindDirection"
    ADD CONSTRAINT "WindDirection_pkey" PRIMARY KEY ("idWinddir");


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: knox_authtoken knox_authtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knox_authtoken
    ADD CONSTRAINT knox_authtoken_pkey PRIMARY KEY (digest);


--
-- Name: volcanoApp_mapping volcanoApp_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."volcanoApp_mapping"
    ADD CONSTRAINT "volcanoApp_mapping_pkey" PRIMARY KEY ("tablenameMap");


--
-- Name: AlertConfiguration_idVolcano_049feca2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "AlertConfiguration_idVolcano_049feca2_like" ON public."AlertConfiguration" USING btree ("idVolcano" varchar_pattern_ops);


--
-- Name: Alert_idAshDispersion_5d781fe0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Alert_idAshDispersion_5d781fe0" ON public."Alert" USING btree ("idAshDispersion");


--
-- Name: Alert_idAshDispersion_5d781fe0_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Alert_idAshDispersion_5d781fe0_like" ON public."Alert" USING btree ("idAshDispersion" varchar_pattern_ops);


--
-- Name: Alert_idPhoto_4dbd2b5e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Alert_idPhoto_4dbd2b5e" ON public."Alert" USING btree ("idPhoto");


--
-- Name: Alert_idPhoto_4dbd2b5e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Alert_idPhoto_4dbd2b5e_like" ON public."Alert" USING btree ("idPhoto" varchar_pattern_ops);


--
-- Name: Alert_idStation_2b1e6b19; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Alert_idStation_2b1e6b19" ON public."Alert" USING btree ("idStation");


--
-- Name: Alert_idStation_2b1e6b19_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Alert_idStation_2b1e6b19_like" ON public."Alert" USING btree ("idStation" varchar_pattern_ops);


--
-- Name: AshDispersion_idAshDispersion_29cde005_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "AshDispersion_idAshDispersion_29cde005_like" ON public."AshDispersion" USING btree ("idAshDispersion" varchar_pattern_ops);


--
-- Name: AshDispersion_idVolcano_867dbae0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "AshDispersion_idVolcano_867dbae0" ON public."AshDispersion" USING btree ("idVolcano");


--
-- Name: AshDispersion_idVolcano_867dbae0_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "AshDispersion_idVolcano_867dbae0_like" ON public."AshDispersion" USING btree ("idVolcano" varchar_pattern_ops);


--
-- Name: AshFallPrediction_idAshfallprediction_ffc51f2b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "AshFallPrediction_idAshfallprediction_ffc51f2b_like" ON public."AshFallPrediction" USING btree ("idAshfallprediction" varchar_pattern_ops);


--
-- Name: AshFallPrediction_idVolcano_192ccacd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "AshFallPrediction_idVolcano_192ccacd" ON public."AshFallPrediction" USING btree ("idVolcano");


--
-- Name: AshFallPrediction_idVolcano_192ccacd_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "AshFallPrediction_idVolcano_192ccacd_like" ON public."AshFallPrediction" USING btree ("idVolcano" varchar_pattern_ops);


--
-- Name: IX_Relationship1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "IX_Relationship1" ON public."Blob" USING btree ("idMask");


--
-- Name: IX_Relationship11; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "IX_Relationship11" ON public."Alert" USING btree ("idVolcano");


--
-- Name: IX_Relationship12; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "IX_Relationship12" ON public."Alert" USING btree ("idAlertConf");


--
-- Name: IX_Relationship14; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "IX_Relationship14" ON public."History" USING btree ("idUser");


--
-- Name: ImageSegmentation_idStation_2f92367c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ImageSegmentation_idStation_2f92367c" ON public."ImageSegmentation" USING btree ("idStation");


--
-- Name: ImageSegmentation_idStation_2f92367c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ImageSegmentation_idStation_2f92367c_like" ON public."ImageSegmentation" USING btree ("idStation" varchar_pattern_ops);


--
-- Name: Mask_idStation_c16ff718; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Mask_idStation_c16ff718" ON public."Mask" USING btree ("idStation");


--
-- Name: Mask_idStation_c16ff718_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Mask_idStation_c16ff718_like" ON public."Mask" USING btree ("idStation" varchar_pattern_ops);


--
-- Name: Station_idVolcano_da91b174; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Station_idVolcano_da91b174" ON public."Station" USING btree ("idVolcano");


--
-- Name: Station_idVolcano_da91b174_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "Station_idVolcano_da91b174_like" ON public."Station" USING btree ("idVolcano" varchar_pattern_ops);


--
-- Name: User_email_667201b5_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "User_email_667201b5_like" ON public."User" USING btree (email varchar_pattern_ops);


--
-- Name: WindDirection_idVolcano_bae26f62; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "WindDirection_idVolcano_bae26f62" ON public."WindDirection" USING btree ("idVolcano");


--
-- Name: WindDirection_idVolcano_bae26f62_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "WindDirection_idVolcano_bae26f62_like" ON public."WindDirection" USING btree ("idVolcano" varchar_pattern_ops);


--
-- Name: WindDirection_idWinddirereorologicalData_d3551def_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "WindDirection_idWinddirereorologicalData_d3551def_like" ON public."WindDirection" USING btree ("idWinddir" varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: knox_authtoken_digest_188c7e77_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_digest_188c7e77_like ON public.knox_authtoken USING btree (digest varchar_pattern_ops);


--
-- Name: knox_authtoken_token_key_8f4f7d47; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_token_key_8f4f7d47 ON public.knox_authtoken USING btree (token_key);


--
-- Name: knox_authtoken_token_key_8f4f7d47_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_token_key_8f4f7d47_like ON public.knox_authtoken USING btree (token_key varchar_pattern_ops);


--
-- Name: knox_authtoken_user_id_e5a5d899; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX knox_authtoken_user_id_e5a5d899 ON public.knox_authtoken USING btree (user_id);


--
-- Name: volcanoApp_mapping_tablenameMap_9392fc03_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "volcanoApp_mapping_tablenameMap_9392fc03_like" ON public."volcanoApp_mapping" USING btree ("tablenameMap" varchar_pattern_ops);


--
-- Name: AlertConfiguration AlertConfiguration_idVolcano_049feca2_fk_Volcano_idVolcano; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AlertConfiguration"
    ADD CONSTRAINT "AlertConfiguration_idVolcano_049feca2_fk_Volcano_idVolcano" FOREIGN KEY ("idVolcano") REFERENCES public."Volcano"("idVolcano") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Alert Alert_idAlertConf_a8d34f90_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Alert"
    ADD CONSTRAINT "Alert_idAlertConf_a8d34f90_fk" FOREIGN KEY ("idAlertConf") REFERENCES public."AlertConfiguration"("idAlertConf") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Alert Alert_idAshDispersion_5d781fe0_fk_AshDispersion_idAshDispersion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Alert"
    ADD CONSTRAINT "Alert_idAshDispersion_5d781fe0_fk_AshDispersion_idAshDispersion" FOREIGN KEY ("idAshDispersion") REFERENCES public."AshDispersion"("idAshDispersion") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Alert Alert_idPhoto_4dbd2b5e_fk_ImageSegmentation_idPhoto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Alert"
    ADD CONSTRAINT "Alert_idPhoto_4dbd2b5e_fk_ImageSegmentation_idPhoto" FOREIGN KEY ("idPhoto") REFERENCES public."ImageSegmentation"("idPhoto") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Alert Alert_idStation_2b1e6b19_fk_Station_idStation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Alert"
    ADD CONSTRAINT "Alert_idStation_2b1e6b19_fk_Station_idStation" FOREIGN KEY ("idStation") REFERENCES public."Station"("idStation") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Alert Alert_idVolcano_6b6ebd91_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Alert"
    ADD CONSTRAINT "Alert_idVolcano_6b6ebd91_fk" FOREIGN KEY ("idVolcano") REFERENCES public."Volcano"("idVolcano") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: AshDispersion AshDispersion_idVolcano_867dbae0_fk_Volcano_idVolcano; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AshDispersion"
    ADD CONSTRAINT "AshDispersion_idVolcano_867dbae0_fk_Volcano_idVolcano" FOREIGN KEY ("idVolcano") REFERENCES public."Volcano"("idVolcano") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: AshFallPrediction AshFallPrediction_idVolcano_192ccacd_fk_Volcano_idVolcano; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AshFallPrediction"
    ADD CONSTRAINT "AshFallPrediction_idVolcano_192ccacd_fk_Volcano_idVolcano" FOREIGN KEY ("idVolcano") REFERENCES public."Volcano"("idVolcano") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Blob Blob_idMask_a8ac3d43_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Blob"
    ADD CONSTRAINT "Blob_idMask_a8ac3d43_fk" FOREIGN KEY ("idMask") REFERENCES public."Mask"("idMask") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ImageSegmentation ImageSegmentation_idStation_2f92367c_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ImageSegmentation"
    ADD CONSTRAINT "ImageSegmentation_idStation_2f92367c_fk" FOREIGN KEY ("idStation") REFERENCES public."Station"("idStation") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Mask Mask_idMask_b324e1c9_fk_ImageSegmentation_idPhoto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Mask"
    ADD CONSTRAINT "Mask_idMask_b324e1c9_fk_ImageSegmentation_idPhoto" FOREIGN KEY ("idMask") REFERENCES public."ImageSegmentation"("idPhoto") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Mask Mask_idStation_c16ff718_fk_Station_idStation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Mask"
    ADD CONSTRAINT "Mask_idStation_c16ff718_fk_Station_idStation" FOREIGN KEY ("idStation") REFERENCES public."Station"("idStation") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: History Relationship14; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."History"
    ADD CONSTRAINT "Relationship14" FOREIGN KEY ("idUser") REFERENCES public."User"(id_id);


--
-- Name: Station Station_idVolcano_da91b174_fk_Volcano_idVolcano; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Station"
    ADD CONSTRAINT "Station_idVolcano_da91b174_fk_Volcano_idVolcano" FOREIGN KEY ("idVolcano") REFERENCES public."Volcano"("idVolcano") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: User User_id_id_cd9ea8e5_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_id_id_cd9ea8e5_fk_auth_user_id" FOREIGN KEY (id_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: WindDirection WindDirection_idVolcano_bae26f62_fk_Volcano_idVolcano; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."WindDirection"
    ADD CONSTRAINT "WindDirection_idVolcano_bae26f62_fk_Volcano_idVolcano" FOREIGN KEY ("idVolcano") REFERENCES public."Volcano"("idVolcano") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Explosion explosion_imagesegmentation_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Explosion"
    ADD CONSTRAINT explosion_imagesegmentation_fk FOREIGN KEY ("idImage") REFERENCES public."ImageSegmentation"("idPhoto");


--
-- Name: Explosion explosion_station_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Explosion"
    ADD CONSTRAINT explosion_station_fk FOREIGN KEY ("idStation") REFERENCES public."Station"("idStation");


--
-- Name: Explosion fk_explosion_ashdispersion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Explosion"
    ADD CONSTRAINT fk_explosion_ashdispersion FOREIGN KEY ("idAshDispersion") REFERENCES public."AshDispersion"("idAshDispersion");


--
-- Name: Explosion fk_explosion_ashfallprediction; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Explosion"
    ADD CONSTRAINT fk_explosion_ashfallprediction FOREIGN KEY ("idAshfallprediction") REFERENCES public."AshFallPrediction"("idAshfallprediction");


--
-- Name: Explosion fk_explosion_volcano; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Explosion"
    ADD CONSTRAINT fk_explosion_volcano FOREIGN KEY ("idVolcano") REFERENCES public."Volcano"("idVolcano");


--
-- Name: Explosion fk_explosion_winddir; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Explosion"
    ADD CONSTRAINT fk_explosion_winddir FOREIGN KEY ("idWinddir") REFERENCES public."WindDirection"("idWinddir");


--
-- Name: knox_authtoken knox_authtoken_user_id_e5a5d899_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knox_authtoken
    ADD CONSTRAINT knox_authtoken_user_id_e5a5d899_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

