--
-- PostgreSQL database dump
--

\restrict BVyLBOn5317IiZioGNB9D6vdfftfPpAUwRBuinkhasA6YI9WkmIovTbBb5TqQeT

-- Dumped from database version 16.9 (165f042)
-- Dumped by pg_dump version 16.10 (Homebrew)

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

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: doctor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.doctor (
    doctor_id uuid DEFAULT gen_random_uuid() NOT NULL,
    full_name text NOT NULL,
    email text,
    phone text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: doctor_patient; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.doctor_patient (
    doctor_patient_id uuid DEFAULT gen_random_uuid() NOT NULL,
    doctor_id uuid NOT NULL,
    patient_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: form; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.form (
    form_id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid NOT NULL,
    submitted_at timestamp with time zone DEFAULT now() NOT NULL,
    doctor_id uuid
);


--
-- Name: form_medication; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.form_medication (
    form_medication_id uuid DEFAULT gen_random_uuid() NOT NULL,
    form_id uuid NOT NULL,
    medication_id uuid NOT NULL
);


--
-- Name: form_symptom; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.form_symptom (
    form_symptom_id uuid DEFAULT gen_random_uuid() NOT NULL,
    form_id uuid NOT NULL,
    symptom_id uuid NOT NULL
);


--
-- Name: medication; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medication (
    medication_id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    strength integer,
    frequency integer,
    duration integer
);


--
-- Name: patient; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patient (
    patient_id uuid DEFAULT gen_random_uuid() NOT NULL,
    full_name text NOT NULL,
    dob date,
    sex_at_birth text,
    phone text,
    email text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: symptom; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.symptom (
    symptom_id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    duration integer,
    intensity integer,
    recurrence boolean
);


--
-- Data for Name: doctor; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.doctor (doctor_id, full_name, email, phone, created_at) FROM stdin;
676399a7-81a2-4f04-b557-1024ab7d9ac7	Andrea Pearson	tpayne@example.org	\N	2025-10-11 16:03:22.041583+00
20dee87d-3bb3-4d4a-8a45-61cfb2fe5820	Timothy Hansen	angelaroberts@example.org	\N	2025-10-11 16:03:22.041583+00
ca24600a-7ab4-403f-8e17-8d1396acfc66	Patrick Freeman	smithcrystal@example.com	\N	2025-10-11 16:03:22.041583+00
8ab87dbb-608b-4777-88bb-f428075eecd8	Derrick Johnson	olee@example.net	\N	2025-10-11 16:03:22.041583+00
c739da48-4642-47f8-a302-7c5159b4514d	Melissa Allison	darrellkerr@example.org	\N	2025-10-11 16:03:22.041583+00
\.


--
-- Data for Name: doctor_patient; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.doctor_patient (doctor_patient_id, doctor_id, patient_id, created_at) FROM stdin;
89165304-05df-4a11-9f08-6c539f6c37b7	676399a7-81a2-4f04-b557-1024ab7d9ac7	9fa8ddc3-2471-49df-a781-4078ad118ed1	2025-10-11 16:03:22.041583+00
9007ffa8-d25a-43b4-a964-6676d10e54ff	20dee87d-3bb3-4d4a-8a45-61cfb2fe5820	8cf9462e-4882-4eb6-8113-03b6627ad6ad	2025-10-11 16:03:22.041583+00
a2a91abb-0312-480f-babd-022d708cb93a	ca24600a-7ab4-403f-8e17-8d1396acfc66	9b18fde8-5e9e-4ee9-9663-cd5f67b58bb6	2025-10-11 16:03:22.041583+00
51977326-9681-43a7-a477-924ab731291a	8ab87dbb-608b-4777-88bb-f428075eecd8	910684f0-8f36-44ea-aea7-953dc37f945b	2025-10-11 16:03:22.041583+00
ab44095e-878a-408d-a643-a133f43a5345	c739da48-4642-47f8-a302-7c5159b4514d	8615e097-7f83-4daf-8138-a33d111aa15b	2025-10-11 16:03:22.041583+00
\.


--
-- Data for Name: form; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.form (form_id, patient_id, submitted_at, doctor_id) FROM stdin;
314d2d6b-5c2f-4a5a-8c8d-cd37184afc11	4dd0edf9-967e-4799-9f5a-83b0e0fe277b	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
ebbf3f68-dc56-4b25-8ede-44df8a26d83d	32c0118d-67b7-4a60-af66-a6909ffe9985	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
f6e7a11c-442e-4259-ab6b-c22083d2c4cd	4dd0edf9-967e-4799-9f5a-83b0e0fe277b	2025-10-11 16:03:22.041583+00	20dee87d-3bb3-4d4a-8a45-61cfb2fe5820
42d55efa-55ec-4169-bcd8-97d2b7491496	c8229e88-afe4-431f-aba8-8f6d5335b41b	2025-10-11 16:03:22.041583+00	c739da48-4642-47f8-a302-7c5159b4514d
bc77f0fc-bc99-407a-9b4c-2db628062693	ba10a6ab-185e-48f7-9aea-8de8d33fefd5	2025-10-11 16:03:22.041583+00	c739da48-4642-47f8-a302-7c5159b4514d
707ec071-8c92-4a69-bb92-3f581da690c8	1601ccaa-ed9a-45ae-bc62-5c270b454fcc	2025-10-11 16:03:22.041583+00	c739da48-4642-47f8-a302-7c5159b4514d
e66be7bb-5c94-475a-844a-1a9621c71b23	910684f0-8f36-44ea-aea7-953dc37f945b	2025-10-11 16:03:22.041583+00	20dee87d-3bb3-4d4a-8a45-61cfb2fe5820
f55fbf85-a1bf-4214-aa10-85f625b91750	32c0118d-67b7-4a60-af66-a6909ffe9985	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
2d0b6cff-7034-4c68-ba09-d224b7beff4f	c8229e88-afe4-431f-aba8-8f6d5335b41b	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
65d2f7f7-ebc7-440c-b0c8-c4df84896953	02bf5421-d1f9-452b-9c05-35beba679e98	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
1470396a-881b-4317-abbb-fffc41525456	8cf9462e-4882-4eb6-8113-03b6627ad6ad	2025-10-11 16:03:22.041583+00	676399a7-81a2-4f04-b557-1024ab7d9ac7
fa0535d2-dc4b-47f1-a582-ea1f9a963b61	adf8d6cf-4ad6-409d-85b4-ae4154010c32	2025-10-11 16:03:22.041583+00	ca24600a-7ab4-403f-8e17-8d1396acfc66
41ce2d2a-3b6e-41af-ad6d-aa42b035561f	43c615a9-cabf-4976-a08a-5e064cb16474	2025-10-11 16:03:22.041583+00	20dee87d-3bb3-4d4a-8a45-61cfb2fe5820
e23d4c44-f6cf-41dd-be59-54d3cbf2d4b2	9b18fde8-5e9e-4ee9-9663-cd5f67b58bb6	2025-10-11 16:03:22.041583+00	ca24600a-7ab4-403f-8e17-8d1396acfc66
ded1ea9b-b4bd-4297-82f5-8269ad082440	7e351f3f-c4ea-4a8f-84c4-e0837844b848	2025-10-11 16:03:22.041583+00	ca24600a-7ab4-403f-8e17-8d1396acfc66
406a6be6-aff3-4c69-9b04-96e2f809dc0f	1601ccaa-ed9a-45ae-bc62-5c270b454fcc	2025-10-11 16:03:22.041583+00	c739da48-4642-47f8-a302-7c5159b4514d
43d4c9e8-0ca9-4d38-bac7-4ec78cbe6bab	592c6f6b-71ab-4a8c-8147-503ebeebbe9b	2025-10-11 16:03:22.041583+00	ca24600a-7ab4-403f-8e17-8d1396acfc66
e623cc24-1e69-4de3-babc-c828d3113a0f	4dd0edf9-967e-4799-9f5a-83b0e0fe277b	2025-10-11 16:03:22.041583+00	ca24600a-7ab4-403f-8e17-8d1396acfc66
5ce00e80-ed41-46c3-8bd1-0df16cb08c30	8615e097-7f83-4daf-8138-a33d111aa15b	2025-10-11 16:03:22.041583+00	20dee87d-3bb3-4d4a-8a45-61cfb2fe5820
f46d11cd-ac55-4b76-a625-ec8011c2585d	02bf5421-d1f9-452b-9c05-35beba679e98	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
6832ebfb-248d-48e1-8654-1b8935e99699	43c615a9-cabf-4976-a08a-5e064cb16474	2025-10-11 16:03:22.041583+00	20dee87d-3bb3-4d4a-8a45-61cfb2fe5820
e668229c-3270-4817-bb95-ee88ebf8e06d	ba10a6ab-185e-48f7-9aea-8de8d33fefd5	2025-10-11 16:03:22.041583+00	20dee87d-3bb3-4d4a-8a45-61cfb2fe5820
184d9c8f-19a5-4096-9f6e-d3593487aeef	7e351f3f-c4ea-4a8f-84c4-e0837844b848	2025-10-11 16:03:22.041583+00	ca24600a-7ab4-403f-8e17-8d1396acfc66
d2610311-ad90-4724-b189-14865fe83b22	adf8d6cf-4ad6-409d-85b4-ae4154010c32	2025-10-11 16:03:22.041583+00	c739da48-4642-47f8-a302-7c5159b4514d
78299058-8e84-46d5-85d7-f1d5712d04f6	22643691-4ca7-4a73-bbda-d64d8f52c360	2025-10-11 16:03:22.041583+00	c739da48-4642-47f8-a302-7c5159b4514d
b8315522-1034-4988-8a57-d37399386b3d	43c615a9-cabf-4976-a08a-5e064cb16474	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
46887419-818c-44b5-ac03-2fe2dc89f31c	592c6f6b-71ab-4a8c-8147-503ebeebbe9b	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
daef211d-8e0d-4e58-8bd5-00a21991be32	7e351f3f-c4ea-4a8f-84c4-e0837844b848	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
70168c2c-2d66-4ba0-860f-531e9457d548	9b18fde8-5e9e-4ee9-9663-cd5f67b58bb6	2025-10-11 16:03:22.041583+00	8ab87dbb-608b-4777-88bb-f428075eecd8
bdbdc92b-af37-4d18-9f36-e61911ee8894	adf8d6cf-4ad6-409d-85b4-ae4154010c32	2025-10-11 16:03:22.041583+00	20dee87d-3bb3-4d4a-8a45-61cfb2fe5820
\.


--
-- Data for Name: form_medication; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.form_medication (form_medication_id, form_id, medication_id) FROM stdin;
\.


--
-- Data for Name: form_symptom; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.form_symptom (form_symptom_id, form_id, symptom_id) FROM stdin;
3691f41a-3109-40ae-a5ef-8ad7b0eddcef	314d2d6b-5c2f-4a5a-8c8d-cd37184afc11	f38a7e49-8ff1-4f6a-8f0f-a10a81906721
f6340d39-7379-4b34-a5e4-453bd0880275	ebbf3f68-dc56-4b25-8ede-44df8a26d83d	b7ed9936-c522-4288-a09c-942ceb09c92a
f25827fc-3e33-4d5b-b1d4-4e2512323c9a	f6e7a11c-442e-4259-ab6b-c22083d2c4cd	922cc9ef-0db1-49f3-baf1-9b5e05512261
51d11025-06c8-4a47-8679-47da6518086e	42d55efa-55ec-4169-bcd8-97d2b7491496	cbb26aa2-3eaf-4f1e-ab8d-5afcf65f3a28
57de3125-4efb-485e-b0c2-37e7a15afa3c	bc77f0fc-bc99-407a-9b4c-2db628062693	abcd998f-793c-4bdd-8c57-7732b85f502c
9827ffae-6ded-46b6-8992-6fc7b4ba7192	707ec071-8c92-4a69-bb92-3f581da690c8	82ab792a-3c3d-4d7f-9db7-99aa31bfb8df
80964dce-6bd8-42a8-b792-4c6152856d76	e66be7bb-5c94-475a-844a-1a9621c71b23	8bd3b785-8ae1-4670-8b0b-055b231d15c4
803010ee-9345-42e8-81d0-f3f0de428b4c	f55fbf85-a1bf-4214-aa10-85f625b91750	b7ed9936-c522-4288-a09c-942ceb09c92a
8ef1d5a7-7628-44fb-98f2-ec60352f31a3	2d0b6cff-7034-4c68-ba09-d224b7beff4f	40b6dbcc-f849-4ae1-b15d-e6a278ebeeb4
8ff63af5-5102-4876-9b8b-1c6fe59930d5	65d2f7f7-ebc7-440c-b0c8-c4df84896953	fb2ab7f3-5319-4b34-b9d3-c1f99a595bfa
10eb413a-def4-49b1-8cf5-49f6d808e684	1470396a-881b-4317-abbb-fffc41525456	fb2ab7f3-5319-4b34-b9d3-c1f99a595bfa
d8aadddc-2c08-4f92-8287-f0aec87c247a	fa0535d2-dc4b-47f1-a582-ea1f9a963b61	6aa229e7-d47d-4dc2-875e-da082dc230a7
524e5835-4e31-423d-8bc8-996ee68aed8b	41ce2d2a-3b6e-41af-ad6d-aa42b035561f	c470b807-06e5-4956-bc9f-ab44e92c8962
49f94c3d-1c6a-4351-ba89-4b4dd6f3cd4a	e23d4c44-f6cf-41dd-be59-54d3cbf2d4b2	f8a164c6-70b4-47c3-85d8-7a6aed289a0c
a2d8b855-a5b6-4d75-a7f5-21502f0828c5	ded1ea9b-b4bd-4297-82f5-8269ad082440	f25cbdbd-8754-425c-a574-2017eb7c2cb8
2a25e94f-0546-415b-820d-22d840f2d9d6	406a6be6-aff3-4c69-9b04-96e2f809dc0f	40b6dbcc-f849-4ae1-b15d-e6a278ebeeb4
3cdaa3e8-a3ec-4958-b5f2-0685cbaeba4e	43d4c9e8-0ca9-4d38-bac7-4ec78cbe6bab	2066b8a4-8a56-48eb-acca-89f2d7eba0da
3d82e885-a3dd-40a6-a91b-132685596765	e623cc24-1e69-4de3-babc-c828d3113a0f	95892fa4-1dac-4327-a3a7-c8114c903aa4
0d9275d2-6257-42c4-9701-defbd643cb80	5ce00e80-ed41-46c3-8bd1-0df16cb08c30	abcd998f-793c-4bdd-8c57-7732b85f502c
a69d83cd-1c7d-4b1e-8357-076da563f34a	f46d11cd-ac55-4b76-a625-ec8011c2585d	bf3974f5-7f39-4fc2-a327-d62ff3c9924d
071ebe92-e40e-441f-bf6e-554715fe82de	6832ebfb-248d-48e1-8654-1b8935e99699	f8a164c6-70b4-47c3-85d8-7a6aed289a0c
9f5656d9-b1fe-4b65-a50f-94be35485ec1	e668229c-3270-4817-bb95-ee88ebf8e06d	727a2ce7-bfe9-46b9-a6ff-9070719399a5
22e1ba55-1e22-45d0-90df-3a0819bc4998	184d9c8f-19a5-4096-9f6e-d3593487aeef	f8a164c6-70b4-47c3-85d8-7a6aed289a0c
93774211-cdf0-437d-bc9a-099626fc5892	d2610311-ad90-4724-b189-14865fe83b22	f52d6416-a560-4258-ad05-bb5322b6dc5b
5e376694-9f3c-432a-b341-aa567c9e9dd4	78299058-8e84-46d5-85d7-f1d5712d04f6	f38a7e49-8ff1-4f6a-8f0f-a10a81906721
cf8412e2-4605-40b1-b3e2-1fe2a46682ba	b8315522-1034-4988-8a57-d37399386b3d	bf3974f5-7f39-4fc2-a327-d62ff3c9924d
7a13a83e-1114-426c-bcd5-43231725125f	46887419-818c-44b5-ac03-2fe2dc89f31c	fb2ab7f3-5319-4b34-b9d3-c1f99a595bfa
07495e8e-bc46-4538-a194-4d09cb00d47b	daef211d-8e0d-4e58-8bd5-00a21991be32	2c50481e-15db-4ec5-8ab4-1aad6a0f5467
c7d279e9-47b8-496c-9438-9dc71485dc41	70168c2c-2d66-4ba0-860f-531e9457d548	c470b807-06e5-4956-bc9f-ab44e92c8962
ef7aed85-323b-4772-bfdf-631d9f5dedd7	bdbdc92b-af37-4d18-9f36-e61911ee8894	abcd998f-793c-4bdd-8c57-7732b85f502c
\.


--
-- Data for Name: medication; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.medication (medication_id, name, strength, frequency, duration) FROM stdin;
16f0f00c-d692-40bb-b43a-85ecf38a217f	season	5845	6	94
c31d41ee-dcaf-432d-9df1-5cf7e400f83f	let	5672	5	63
ccbdd3ae-8346-4e88-b600-2398cb3560f1	other	9695	4	48
b49960e6-be5c-42bb-ad03-3a0f21b5ab4c	simply	37	8	33
5ceb5090-4efa-4dc8-a0c0-2930841d2b1c	research	3244	10	77
d5d15f96-6d3a-483b-825b-9981470ef9f9	ground	4058	8	80
dad5d8c8-2167-48f6-b8be-9299a7dd0b4a	sport	8139	5	28
5549f229-5519-445b-bce1-16ba92e1cace	one	2301	2	13
1addc352-3712-4f74-904a-1364526317c3	will	5756	1	48
80d7d443-95ca-4290-b369-52f39989b865	which	2130	4	63
bbac18a7-45b9-411f-952d-a9cb8bacf790	oil	7748	7	42
5d30de20-4566-4f21-9cbf-35369cb0a16b	color	4571	3	16
21532c35-cc88-40d5-a564-032ff514c90d	least	3574	2	30
14557dee-a5a6-473d-8676-8f89c56d6eac	attack	566	9	89
dbe36a87-f924-4088-bd8e-4a7246298dbe	six	4682	8	17
ff97046e-0758-4fb0-843e-916af5a362b8	like	8403	9	73
618b3f97-aaa8-4e65-b137-737f066307c9	soon	6303	6	60
af531235-d60b-40cf-ab68-c2938c6af94a	resource	7722	8	25
5248f2e0-0379-4ff8-9963-3e7e3ad8a3c1	future	3930	7	61
61e84b6a-1225-42c9-aac2-3e22510ec1fd	become	9449	2	13
77b94fa0-bb15-405b-83fe-b4dd72044d2f	international	1633	3	68
ae846128-a749-4398-92bd-8b343d3cb18e	but	2798	3	30
df7ae004-8908-4dbb-8299-558b5455551d	voice	6780	7	60
7265c4c6-9670-43b2-8432-355b249f794e	six	6239	2	76
b0385c3e-ad98-4103-9a4a-f4610e83bc8e	buy	4125	8	2
e6105ebf-b680-4263-b77a-6c2f03c850c8	well	934	6	33
66b269fc-65ac-4f65-b4b0-d5476fcef428	father	3560	5	82
2df1aa76-dccd-4df3-9ebb-878a975f8743	group	9491	8	86
9b50482b-7cc6-4caa-8c01-76676c545d83	sometimes	6423	4	74
11a53b43-6602-4848-a6a4-db96fa0ace2f	father	7883	10	55
\.


--
-- Data for Name: patient; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.patient (patient_id, full_name, dob, sex_at_birth, phone, email, created_at) FROM stdin;
469e26cb-65ab-4898-b1f9-cbbe8f6b7d27	Sherry Taylor	1992-06-28	\N	\N	\N	2025-10-11 16:03:22.041583+00
4dd0edf9-967e-4799-9f5a-83b0e0fe277b	Jennifer Rogers	2004-02-07	\N	\N	\N	2025-10-11 16:03:22.041583+00
8cf9462e-4882-4eb6-8113-03b6627ad6ad	Todd Taylor	1944-12-03	\N	\N	\N	2025-10-11 16:03:22.041583+00
c8229e88-afe4-431f-aba8-8f6d5335b41b	Sherri Knight	1972-06-04	\N	\N	\N	2025-10-11 16:03:22.041583+00
ba10a6ab-185e-48f7-9aea-8de8d33fefd5	Alexandra Lee	1982-10-21	\N	\N	\N	2025-10-11 16:03:22.041583+00
adf8d6cf-4ad6-409d-85b4-ae4154010c32	Lucas Harris	2003-05-24	\N	\N	\N	2025-10-11 16:03:22.041583+00
32c0118d-67b7-4a60-af66-a6909ffe9985	Alexis Tucker	1957-03-14	\N	\N	\N	2025-10-11 16:03:22.041583+00
4b47332f-91bf-418c-97cc-73709f51a83b	Richard Castro	1990-03-22	\N	\N	\N	2025-10-11 16:03:22.041583+00
564d4259-480e-417d-acb7-cfacb505a40a	Kyle Walker	1953-04-06	\N	\N	\N	2025-10-11 16:03:22.041583+00
193b7514-7889-4192-9946-11014526ef5a	Brianna Taylor	1972-11-28	\N	\N	\N	2025-10-11 16:03:22.041583+00
43c615a9-cabf-4976-a08a-5e064cb16474	Katelyn Martinez	1987-01-12	\N	\N	\N	2025-10-11 16:03:22.041583+00
8615e097-7f83-4daf-8138-a33d111aa15b	Stacy Johnson	1974-05-29	\N	\N	\N	2025-10-11 16:03:22.041583+00
02bf5421-d1f9-452b-9c05-35beba679e98	Courtney Peck	2003-04-14	\N	\N	\N	2025-10-11 16:03:22.041583+00
22643691-4ca7-4a73-bbda-d64d8f52c360	Jason Chavez	1993-02-26	\N	\N	\N	2025-10-11 16:03:22.041583+00
9fa8ddc3-2471-49df-a781-4078ad118ed1	Miguel Davidson	1955-11-21	\N	\N	\N	2025-10-11 16:03:22.041583+00
9b18fde8-5e9e-4ee9-9663-cd5f67b58bb6	Teresa Galvan	2006-11-12	\N	\N	\N	2025-10-11 16:03:22.041583+00
1601ccaa-ed9a-45ae-bc62-5c270b454fcc	Brandy Cobb	1987-09-22	\N	\N	\N	2025-10-11 16:03:22.041583+00
910684f0-8f36-44ea-aea7-953dc37f945b	Monica Miles	1950-11-20	\N	\N	\N	2025-10-11 16:03:22.041583+00
592c6f6b-71ab-4a8c-8147-503ebeebbe9b	Chris Vance	1980-07-01	\N	\N	\N	2025-10-11 16:03:22.041583+00
7e351f3f-c4ea-4a8f-84c4-e0837844b848	Abigail Trujillo	2003-01-24	\N	\N	\N	2025-10-11 16:03:22.041583+00
\.


--
-- Data for Name: symptom; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.symptom (symptom_id, name, duration, intensity, recurrence) FROM stdin;
ed8bbf30-8f56-4ff3-9bff-3183665049ac	Or run.	63	6	f
f8a164c6-70b4-47c3-85d8-7a6aed289a0c	Same international.	29	2	t
f38a7e49-8ff1-4f6a-8f0f-a10a81906721	Give.	67	3	t
23aeecee-71a2-4674-a6b6-9b068862cf4d	Open forget.	69	2	t
cbb26aa2-3eaf-4f1e-ab8d-5afcf65f3a28	Per site.	51	4	t
727a2ce7-bfe9-46b9-a6ff-9070719399a5	Board natural.	3	9	f
fb2ab7f3-5319-4b34-b9d3-c1f99a595bfa	What.	4	8	f
c470b807-06e5-4956-bc9f-ab44e92c8962	Bit.	95	9	f
82ab792a-3c3d-4d7f-9db7-99aa31bfb8df	May.	68	2	t
2c50481e-15db-4ec5-8ab4-1aad6a0f5467	As.	77	7	f
7188f94e-ab97-41f9-9772-e3e197f7f88d	Democratic.	23	6	f
99feff52-c767-400b-b8fc-8e0ac4bbfda4	Fine where.	63	7	f
bf3974f5-7f39-4fc2-a327-d62ff3c9924d	Cause born.	45	10	t
8bd3b785-8ae1-4670-8b0b-055b231d15c4	So.	89	5	f
a803a116-3d57-4061-aa53-6257052abe67	Enter.	38	4	t
b7ed9936-c522-4288-a09c-942ceb09c92a	Mother.	28	4	t
2066b8a4-8a56-48eb-acca-89f2d7eba0da	Pass daughter.	24	1	t
f0ebe1d5-a800-40b1-8eea-d1dd1df17bab	Forget administration.	41	4	t
6aa229e7-d47d-4dc2-875e-da082dc230a7	Actually second.	40	7	t
f52d6416-a560-4258-ad05-bb5322b6dc5b	Feeling.	80	7	f
9d141050-688f-4c71-92c6-722438ba77d5	Everyone describe.	89	1	f
40b6dbcc-f849-4ae1-b15d-e6a278ebeeb4	Region perhaps.	40	1	t
95892fa4-1dac-4327-a3a7-c8114c903aa4	Building.	73	4	f
5e5d8360-0553-49b3-bcd7-badebf9c34c8	Feeling.	77	6	f
f25cbdbd-8754-425c-a574-2017eb7c2cb8	Eight hear.	49	6	f
e9863b54-877f-4b1e-a0a6-c6e70e2f5168	What operation.	45	9	f
e09b5c29-a296-4ee3-a665-83e3e94792d8	Key difficult.	26	9	f
c7db6d9e-0e48-41ca-ba0c-51bb77b5822a	Play.	39	3	f
abcd998f-793c-4bdd-8c57-7732b85f502c	Voice.	82	6	f
922cc9ef-0db1-49f3-baf1-9b5e05512261	Between approach.	97	4	f
\.


--
-- Name: doctor doctor_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_email_key UNIQUE (email);


--
-- Name: doctor_patient doctor_patient_doctor_id_patient_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doctor_patient
    ADD CONSTRAINT doctor_patient_doctor_id_patient_id_key UNIQUE (doctor_id, patient_id);


--
-- Name: doctor_patient doctor_patient_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doctor_patient
    ADD CONSTRAINT doctor_patient_pkey PRIMARY KEY (doctor_patient_id);


--
-- Name: doctor doctor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_pkey PRIMARY KEY (doctor_id);


--
-- Name: form_medication form_medication_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_medication
    ADD CONSTRAINT form_medication_pkey PRIMARY KEY (form_medication_id);


--
-- Name: form form_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_pkey PRIMARY KEY (form_id);


--
-- Name: form_symptom form_symptom_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_symptom
    ADD CONSTRAINT form_symptom_pkey PRIMARY KEY (form_symptom_id);


--
-- Name: medication medication_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medication
    ADD CONSTRAINT medication_pkey PRIMARY KEY (medication_id);


--
-- Name: patient patient_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);


--
-- Name: symptom symptom_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.symptom
    ADD CONSTRAINT symptom_pkey PRIMARY KEY (symptom_id);


--
-- Name: idx_doctor_patient_doctor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_doctor_patient_doctor ON public.doctor_patient USING btree (doctor_id);


--
-- Name: idx_doctor_patient_patient; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_doctor_patient_patient ON public.doctor_patient USING btree (patient_id);


--
-- Name: idx_form_by_patient; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_form_by_patient ON public.form USING btree (patient_id);


--
-- Name: idx_form_med_form; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_form_med_form ON public.form_medication USING btree (form_id);


--
-- Name: idx_form_med_medication; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_form_med_medication ON public.form_medication USING btree (medication_id);


--
-- Name: idx_form_sym_form; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_form_sym_form ON public.form_symptom USING btree (form_id);


--
-- Name: idx_form_sym_symptom; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_form_sym_symptom ON public.form_symptom USING btree (symptom_id);


--
-- Name: doctor_patient doctor_patient_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doctor_patient
    ADD CONSTRAINT doctor_patient_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id) ON DELETE CASCADE;


--
-- Name: doctor_patient doctor_patient_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doctor_patient
    ADD CONSTRAINT doctor_patient_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id) ON DELETE CASCADE;


--
-- Name: form form_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
-- Name: form_medication form_medication_form_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_medication
    ADD CONSTRAINT form_medication_form_id_fkey FOREIGN KEY (form_id) REFERENCES public.form(form_id) ON DELETE CASCADE;


--
-- Name: form_medication form_medication_medication_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_medication
    ADD CONSTRAINT form_medication_medication_id_fkey FOREIGN KEY (medication_id) REFERENCES public.medication(medication_id) ON DELETE CASCADE;


--
-- Name: form form_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id) ON DELETE CASCADE;


--
-- Name: form_symptom form_symptom_form_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_symptom
    ADD CONSTRAINT form_symptom_form_id_fkey FOREIGN KEY (form_id) REFERENCES public.form(form_id) ON DELETE CASCADE;


--
-- Name: form_symptom form_symptom_symptom_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_symptom
    ADD CONSTRAINT form_symptom_symptom_id_fkey FOREIGN KEY (symptom_id) REFERENCES public.symptom(symptom_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict BVyLBOn5317IiZioGNB9D6vdfftfPpAUwRBuinkhasA6YI9WkmIovTbBb5TqQeT

