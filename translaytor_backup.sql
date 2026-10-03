--
-- PostgreSQL database dump
--

\restrict VCb2wQwf0JAgrUYon3fGvyYcCfrVSS1LGTvZGxKYBOmS0uGLDFQsQgiCWvf4gsq

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: daily_goal; Type: TABLE; Schema: public; Owner: translaytor
--

CREATE TABLE public.daily_goal (
    telegram_id bigint NOT NULL,
    goal_date date NOT NULL,
    completed integer DEFAULT 0,
    target integer DEFAULT 10
);


ALTER TABLE public.daily_goal OWNER TO translaytor;

--
-- Name: history; Type: TABLE; Schema: public; Owner: translaytor
--

CREATE TABLE public.history (
    id integer NOT NULL,
    telegram_id bigint,
    original_text text,
    translated_text text,
    created_at timestamp without time zone DEFAULT now(),
    favorite boolean DEFAULT false,
    study_known integer DEFAULT 0,
    study_unknown integer DEFAULT 0,
    last_review timestamp without time zone,
    next_review timestamp without time zone,
    review_interval integer DEFAULT 1
);


ALTER TABLE public.history OWNER TO translaytor;

--
-- Name: history_id_seq; Type: SEQUENCE; Schema: public; Owner: translaytor
--

CREATE SEQUENCE public.history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.history_id_seq OWNER TO translaytor;

--
-- Name: history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: translaytor
--

ALTER SEQUENCE public.history_id_seq OWNED BY public.history.id;


--
-- Name: learning_session; Type: TABLE; Schema: public; Owner: translaytor
--

CREATE TABLE public.learning_session (
    telegram_id bigint NOT NULL,
    category character varying(50),
    level character varying(10),
    updated_at timestamp without time zone DEFAULT now(),
    mode text DEFAULT 'new'::text
);


ALTER TABLE public.learning_session OWNER TO translaytor;

--
-- Name: study_session; Type: TABLE; Schema: public; Owner: translaytor
--

CREATE TABLE public.study_session (
    telegram_id bigint NOT NULL,
    total_answers integer DEFAULT 0,
    correct_answers integer DEFAULT 0,
    wrong_answers integer DEFAULT 0
);


ALTER TABLE public.study_session OWNER TO translaytor;

--
-- Name: user_words; Type: TABLE; Schema: public; Owner: translaytor
--

CREATE TABLE public.user_words (
    id integer NOT NULL,
    telegram_id bigint NOT NULL,
    word_id integer NOT NULL,
    known integer DEFAULT 0,
    unknown integer DEFAULT 0,
    next_review timestamp without time zone DEFAULT now()
);


ALTER TABLE public.user_words OWNER TO translaytor;

--
-- Name: user_words_id_seq; Type: SEQUENCE; Schema: public; Owner: translaytor
--

CREATE SEQUENCE public.user_words_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_words_id_seq OWNER TO translaytor;

--
-- Name: user_words_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: translaytor
--

ALTER SEQUENCE public.user_words_id_seq OWNED BY public.user_words.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: translaytor
--

CREATE TABLE public.users (
    telegram_id bigint NOT NULL,
    language character varying(10) DEFAULT 'en'::character varying,
    xp integer DEFAULT 0,
    streak integer DEFAULT 0,
    last_activity date,
    voice_enabled boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO translaytor;

--
-- Name: word_progress; Type: TABLE; Schema: public; Owner: translaytor
--

CREATE TABLE public.word_progress (
    id integer NOT NULL,
    telegram_id bigint NOT NULL,
    word_id integer NOT NULL,
    learned boolean DEFAULT false,
    correct_answers integer DEFAULT 0,
    wrong_answers integer DEFAULT 0,
    next_review timestamp without time zone DEFAULT now(),
    streak integer DEFAULT 0,
    learning_stage integer DEFAULT 1
);


ALTER TABLE public.word_progress OWNER TO translaytor;

--
-- Name: word_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: translaytor
--

CREATE SEQUENCE public.word_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.word_progress_id_seq OWNER TO translaytor;

--
-- Name: word_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: translaytor
--

ALTER SEQUENCE public.word_progress_id_seq OWNED BY public.word_progress.id;


--
-- Name: words; Type: TABLE; Schema: public; Owner: translaytor
--

CREATE TABLE public.words (
    id integer NOT NULL,
    word text NOT NULL,
    translation text NOT NULL,
    language text NOT NULL,
    image_url text,
    level text DEFAULT 1,
    category text,
    audio_url text
);


ALTER TABLE public.words OWNER TO translaytor;

--
-- Name: words_id_seq; Type: SEQUENCE; Schema: public; Owner: translaytor
--

CREATE SEQUENCE public.words_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.words_id_seq OWNER TO translaytor;

--
-- Name: words_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: translaytor
--

ALTER SEQUENCE public.words_id_seq OWNED BY public.words.id;


--
-- Name: history id; Type: DEFAULT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.history ALTER COLUMN id SET DEFAULT nextval('public.history_id_seq'::regclass);


--
-- Name: user_words id; Type: DEFAULT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.user_words ALTER COLUMN id SET DEFAULT nextval('public.user_words_id_seq'::regclass);


--
-- Name: word_progress id; Type: DEFAULT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.word_progress ALTER COLUMN id SET DEFAULT nextval('public.word_progress_id_seq'::regclass);


--
-- Name: words id; Type: DEFAULT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.words ALTER COLUMN id SET DEFAULT nextval('public.words_id_seq'::regclass);


--
-- Data for Name: daily_goal; Type: TABLE DATA; Schema: public; Owner: translaytor
--

COPY public.daily_goal (telegram_id, goal_date, completed, target) FROM stdin;
6599345138	2026-09-23	0	10
\.


--
-- Data for Name: history; Type: TABLE DATA; Schema: public; Owner: translaytor
--

COPY public.history (id, telegram_id, original_text, translated_text, created_at, favorite, study_known, study_unknown, last_review, next_review, review_interval) FROM stdin;
61	8658108870	я в мечети	❌ Не удалось выполнить перевод.\nПопробуйте позже.	2026-07-11 14:17:47.819139	f	0	0	\N	\N	1
63	8658108870	я хочу стать програмистом	I want to become a programmer	2026-07-11 14:21:21.482038	f	0	0	\N	\N	1
65	8658108870	я пишу бот переводчик	I'm writing a bot translator	2026-07-11 14:25:09.495121	f	0	0	\N	\N	1
67	8658108870	яблоко	apple	2026-07-11 14:26:21.346078	f	0	0	\N	\N	1
73	8658108870	танк	tank	2026-07-11 14:35:13.968706	f	0	0	\N	\N	1
76	8658108870	дом	house	2026-07-11 14:46:22.056022	f	0	0	\N	\N	1
79	8658108870	земля	Earth	2026-07-11 14:52:37.224417	f	0	0	\N	\N	1
81	8658108870	кролик	rabbit	2026-07-11 15:02:21.649787	f	0	0	\N	\N	1
\.


--
-- Data for Name: learning_session; Type: TABLE DATA; Schema: public; Owner: translaytor
--

COPY public.learning_session (telegram_id, category, level, updated_at, mode) FROM stdin;
6599345138	food	A1	2026-09-23 11:46:28.481917	new
\.


--
-- Data for Name: study_session; Type: TABLE DATA; Schema: public; Owner: translaytor
--

COPY public.study_session (telegram_id, total_answers, correct_answers, wrong_answers) FROM stdin;
\.


--
-- Data for Name: user_words; Type: TABLE DATA; Schema: public; Owner: translaytor
--

COPY public.user_words (id, telegram_id, word_id, known, unknown, next_review) FROM stdin;
1	6599345138	1	0	0	2026-07-17 11:43:51.787501
2	6599345138	3	0	0	2026-07-17 11:44:08.595637
3	6599345138	908	0	0	2026-07-17 11:44:20.70795
4	6599345138	2110	0	0	2026-08-05 13:49:10.163152
12	6599345138	3937	0	0	2026-08-07 14:58:11.381406
13	6599345138	3938	0	0	2026-08-07 19:19:27.875667
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: translaytor
--

COPY public.users (telegram_id, language, xp, streak, last_activity, voice_enabled) FROM stdin;
8658108870	en	36	0	\N	f
6599345138	en	3204	1	2026-09-23	t
\.


--
-- Data for Name: word_progress; Type: TABLE DATA; Schema: public; Owner: translaytor
--

COPY public.word_progress (id, telegram_id, word_id, learned, correct_answers, wrong_answers, next_review, streak, learning_stage) FROM stdin;
322	6599345138	300	f	3	0	2026-09-15 18:00:03.799016	0	3
298	6599345138	216	t	4	0	2026-10-01 18:00:12.472758	0	4
276	6599345138	3942	t	4	1	2026-08-08 16:08:22.501401	0	4
324	6599345138	296	t	4	1	2026-09-08 17:35:13.873461	0	4
325	6599345138	414	t	4	1	2026-09-08 17:35:15.11179	0	4
326	6599345138	291	f	2	0	2026-08-19 18:01:15.97176	0	2
370	6599345138	270	t	4	1	2026-09-12 15:33:38.241379	0	4
296	6599345138	225	t	4	0	2026-09-14 16:23:33.725965	0	4
397	6599345138	219	t	4	1	2026-09-14 16:41:15.248038	0	4
491	6599345138	140	f	1	0	2026-08-18 16:41:49.28564	0	1
495	6599345138	164	t	4	1	2026-09-14 16:42:58.489236	0	4
494	6599345138	123	t	4	1	2026-09-14 16:43:02.162396	0	4
410	6599345138	227	t	4	1	2026-09-15 14:26:08.270927	0	4
4	6599345138	6	t	2	0	2099-01-01 00:00:00	0	1
288	6599345138	3943	t	4	3	2026-09-08 17:29:03.793105	0	4
301	6599345138	196	t	4	1	2026-09-08 17:29:20.863353	0	4
260	6599345138	3941	t	4	1	2026-09-07 15:59:27.62279	0	4
337	6599345138	369	t	4	2	2026-09-11 18:01:47.101915	0	4
340	6599345138	213	t	4	1	2026-09-11 18:01:50.242113	0	4
160	6599345138	58	t	2	1	2099-01-01 00:00:00	0	0
159	6599345138	3923	t	2	1	2099-01-01 00:00:00	0	0
338	6599345138	260	t	4	2	2026-09-12 15:33:34.080921	0	4
191	6599345138	232	t	1	0	2099-01-01 00:00:00	0	1
148	6599345138	132	t	2	0	2099-01-01 00:00:00	0	1
198	6599345138	210	t	1	0	2099-01-01 00:00:00	0	1
378	6599345138	292	t	4	0	2026-10-01 18:01:44.964109	0	4
208	6599345138	209	t	1	0	2099-01-01 00:00:00	0	1
335	6599345138	376	t	4	0	2026-09-11 18:02:10.852476	0	4
3	6599345138	4	t	2	0	2099-01-01 00:00:00	0	1
161	6599345138	103	t	2	1	2099-01-01 00:00:00	0	0
7	6599345138	5	t	3	0	2099-01-01 00:00:00	0	1
112	6599345138	276	t	1	0	2099-01-01 00:00:00	0	1
48	6599345138	2807	t	5	2	2099-01-01 00:00:00	3	1
77	6599345138	198	t	3	1	2099-01-01 00:00:00	3	1
1	6599345138	2	t	3	1	2099-01-01 00:00:00	0	1
16	6599345138	10	t	1	0	2099-01-01 00:00:00	0	1
18	6599345138	15	t	1	0	2099-01-01 00:00:00	0	1
21	6599345138	11	t	1	0	2099-01-01 00:00:00	0	1
24	6599345138	7	t	1	0	2099-01-01 00:00:00	0	1
25	6599345138	275	t	1	0	2099-01-01 00:00:00	0	1
26	6599345138	118	t	1	0	2099-01-01 00:00:00	0	1
31	6599345138	203	t	1	0	2099-01-01 00:00:00	0	1
32	6599345138	363	t	1	0	2099-01-01 00:00:00	0	1
34	6599345138	287	t	1	0	2099-01-01 00:00:00	0	1
38	6599345138	343	t	1	0	2099-01-01 00:00:00	0	1
39	6599345138	145	t	1	0	2099-01-01 00:00:00	0	1
42	6599345138	174	t	1	0	2099-01-01 00:00:00	0	1
44	6599345138	380	t	1	0	2099-01-01 00:00:00	0	1
45	6599345138	375	t	1	0	2099-01-01 00:00:00	0	1
47	6599345138	377	t	1	0	2099-01-01 00:00:00	0	1
51	6599345138	385	t	1	0	2099-01-01 00:00:00	0	1
55	6599345138	107	t	1	0	2099-01-01 00:00:00	0	1
58	6599345138	2806	t	1	0	2099-01-01 00:00:00	0	1
60	6599345138	328	t	1	0	2099-01-01 00:00:00	0	1
62	6599345138	319	t	1	0	2099-01-01 00:00:00	0	1
63	6599345138	321	t	1	0	2099-01-01 00:00:00	0	1
64	6599345138	200	t	1	0	2099-01-01 00:00:00	0	1
68	6599345138	222	t	1	0	2099-01-01 00:00:00	0	1
72	6599345138	283	t	1	0	2099-01-01 00:00:00	0	1
73	6599345138	269	t	1	0	2099-01-01 00:00:00	0	1
74	6599345138	205	t	1	0	2099-01-01 00:00:00	0	1
75	6599345138	241	t	1	0	2099-01-01 00:00:00	0	1
78	6599345138	236	t	1	0	2099-01-01 00:00:00	0	1
81	6599345138	218	t	1	0	2099-01-01 00:00:00	0	1
84	6599345138	228	t	1	0	2099-01-01 00:00:00	0	1
85	6599345138	257	t	1	0	2099-01-01 00:00:00	0	1
88	6599345138	240	t	1	0	2099-01-01 00:00:00	0	1
90	6599345138	235	t	1	0	2099-01-01 00:00:00	0	1
91	6599345138	197	t	1	0	2099-01-01 00:00:00	0	1
92	6599345138	239	t	1	0	2099-01-01 00:00:00	0	1
94	6599345138	230	t	1	0	2099-01-01 00:00:00	0	1
96	6599345138	370	t	1	0	2099-01-01 00:00:00	0	1
22	6599345138	8	t	2	0	2099-01-01 00:00:00	0	1
37	6599345138	359	t	2	1	2099-01-01 00:00:00	0	1
50	6599345138	374	t	2	0	2099-01-01 00:00:00	0	1
27	6599345138	234	t	2	0	2099-01-01 00:00:00	0	2
76	6599345138	262	t	2	0	2099-01-01 00:00:00	0	2
71	6599345138	271	t	2	0	2099-01-01 00:00:00	0	1
108	6599345138	309	t	1	0	2099-01-01 00:00:00	0	1
49	6599345138	373	t	2	0	2099-01-01 00:00:00	0	1
28	6599345138	1456	t	3	1	2099-01-01 00:00:00	2	1
10	6599345138	1	t	3	2	2099-01-01 00:00:00	0	1
61	6599345138	358	t	3	1	2099-01-01 00:00:00	0	1
80	6599345138	263	t	2	0	2099-01-01 00:00:00	0	1
147	6599345138	117	t	1	0	2099-01-01 00:00:00	0	1
65	6599345138	245	t	2	0	2099-01-01 00:00:00	0	1
150	6599345138	162	t	2	0	2099-01-01 00:00:00	0	1
36	6599345138	302	t	4	2	2099-01-01 00:00:00	3	1
54	6599345138	159	t	2	0	2099-01-01 00:00:00	0	1
70	6599345138	220	t	3	0	2099-01-01 00:00:00	0	1
209	6599345138	3733	t	1	0	2099-01-01 00:00:00	0	1
69	6599345138	206	t	2	0	2099-01-01 00:00:00	0	1
212	6599345138	243	t	1	0	2099-01-01 00:00:00	0	1
190	6599345138	212	t	2	0	2099-01-01 00:00:00	0	1
46	6599345138	379	t	3	0	2099-01-01 00:00:00	0	1
455	6599345138	335	f	3	0	2026-09-18 15:31:29.127992	0	3
405	6599345138	259	t	4	0	2026-10-06 17:01:51.610223	0	4
526	6599345138	2079	f	2	0	2026-09-13 17:18:00.14959	0	2
528	6599345138	3946	f	1	1	2026-09-07 17:18:20.066025	0	0
457	6599345138	290	f	2	0	2026-09-14 20:04:08.628167	0	2
531	6599345138	3949	f	2	0	2026-09-14 20:04:53.111154	0	2
532	6599345138	3950	f	2	0	2026-09-16 19:53:34.785082	0	2
373	6599345138	229	t	5	1	2026-10-19 22:12:57.249216	0	4
372	6599345138	204	t	5	0	2026-10-20 13:19:56.214446	0	4
299	6599345138	208	t	5	1	2026-10-20 13:28:31.887852	0	4
236	6599345138	431	t	1	0	2099-01-01 00:00:00	0	1
238	6599345138	114	t	1	0	2099-01-01 00:00:00	0	1
239	6599345138	391	t	1	0	2099-01-01 00:00:00	0	1
240	6599345138	910	t	1	0	2099-01-01 00:00:00	0	1
241	6599345138	76	t	1	0	2099-01-01 00:00:00	0	1
438	6599345138	336	t	4	1	2026-09-13 17:50:57.086851	0	4
437	6599345138	288	t	4	1	2026-09-13 17:50:52.228736	0	4
439	6599345138	352	t	4	1	2026-09-13 17:50:49.523909	0	4
464	6599345138	244	t	4	2	2026-09-14 16:35:44.299324	0	4
376	6599345138	360	t	4	1	2026-09-15 14:26:27.932664	0	4
59	6599345138	338	t	2	0	2099-01-01 00:00:00	0	1
149	6599345138	173	t	1	0	2099-01-01 00:00:00	0	1
17	6599345138	9	t	2	0	2099-01-01 00:00:00	0	1
19	6599345138	14	t	3	0	2099-01-01 00:00:00	0	3
83	6599345138	221	t	2	0	2099-01-01 00:00:00	0	1
66	6599345138	207	t	2	0	2099-01-01 00:00:00	0	1
153	6599345138	869	t	2	1	2099-01-01 00:00:00	0	0
87	6599345138	217	t	2	0	2099-01-01 00:00:00	0	1
67	6599345138	258	t	2	0	2099-01-01 00:00:00	0	1
156	6599345138	917	t	2	1	2099-01-01 00:00:00	0	0
103	6599345138	304	t	4	1	2099-01-01 00:00:00	3	1
157	6599345138	282	t	2	0	2099-01-01 00:00:00	0	1
33	6599345138	295	t	2	0	2099-01-01 00:00:00	0	1
53	6599345138	298	t	2	0	2099-01-01 00:00:00	0	1
56	6599345138	131	t	3	0	2099-01-01 00:00:00	0	1
89	6599345138	238	t	2	0	2099-01-01 00:00:00	0	1
79	6599345138	242	t	2	0	2099-01-01 00:00:00	0	1
11	6599345138	3	t	2	0	2099-01-01 00:00:00	0	1
105	6599345138	284	t	4	1	2099-01-01 00:00:00	0	1
30	6599345138	895	t	2	0	2099-01-01 00:00:00	0	1
23	6599345138	12	t	2	0	2099-01-01 00:00:00	0	1
93	6599345138	237	t	2	0	2099-01-01 00:00:00	0	1
86	6599345138	274	t	2	0	2099-01-01 00:00:00	0	1
82	6599345138	202	t	3	0	2099-01-01 00:00:00	0	1
95	6599345138	415	t	2	0	2099-01-01 00:00:00	0	1
57	6599345138	160	t	2	0	2099-01-01 00:00:00	0	1
52	6599345138	372	t	3	0	2099-01-01 00:00:00	0	1
162	6599345138	250	t	2	1	2099-01-01 00:00:00	0	0
167	6599345138	44	t	2	1	2099-01-01 00:00:00	0	0
151	6599345138	2087	t	2	1	2099-01-01 00:00:00	0	0
110	6599345138	349	t	2	0	2099-01-01 00:00:00	0	1
166	6599345138	3841	t	2	1	2099-01-01 00:00:00	0	0
29	6599345138	2124	t	2	0	2099-01-01 00:00:00	0	1
158	6599345138	130	t	3	2	2099-01-01 00:00:00	0	0
40	6599345138	120	t	2	0	2099-01-01 00:00:00	0	1
98	6599345138	368	t	2	1	2099-01-01 00:00:00	0	1
43	6599345138	125	t	2	0	2099-01-01 00:00:00	0	2
41	6599345138	189	t	2	0	2099-01-01 00:00:00	0	2
154	6599345138	429	t	2	0	2099-01-01 00:00:00	0	2
35	6599345138	331	t	3	0	2099-01-01 00:00:00	0	3
20	6599345138	13	t	2	0	2099-01-01 00:00:00	0	2
104	6599345138	281	t	5	1	2099-01-01 00:00:00	3	4
101	6599345138	378	t	2	0	2099-01-01 00:00:00	0	2
242	6599345138	187	t	1	0	2099-01-01 00:00:00	0	1
243	6599345138	348	t	1	0	2099-01-01 00:00:00	0	1
244	6599345138	2073	t	1	0	2099-01-01 00:00:00	0	1
245	6599345138	26	t	1	0	2099-01-01 00:00:00	0	1
246	6599345138	3938	t	1	0	2099-01-01 00:00:00	0	1
247	6599345138	3937	t	1	0	2099-01-01 00:00:00	0	1
250	6599345138	2119	t	1	0	2099-01-01 00:00:00	0	1
252	6599345138	3939	t	2	1	2099-01-01 00:00:00	0	2
152	6599345138	231	t	2	0	2099-01-01 00:00:00	0	2
207	6599345138	215	t	2	0	2099-01-01 00:00:00	0	2
256	6599345138	3940	t	2	1	2026-08-09 11:20:30.3448	0	2
305	6599345138	273	t	4	1	2026-09-08 17:29:24.750227	0	4
294	6599345138	3944	f	2	0	2026-08-19 18:01:25.53048	0	2
360	6599345138	371	t	4	0	2026-09-11 18:02:28.562823	0	4
402	6599345138	199	t	4	1	2026-09-14 16:41:27.950318	0	4
362	6599345138	2805	t	4	0	2026-09-11 18:02:43.479464	0	4
527	6599345138	2112	f	0	0	2026-08-19 11:09:06.224272	0	1
308	6599345138	264	t	4	0	2026-10-01 17:59:45.141385	0	4
390	6599345138	157	f	2	0	2026-09-08 18:00:15.763367	0	2
393	6599345138	153	f	2	0	2026-09-08 18:00:49.337872	0	2
395	6599345138	149	f	2	0	2026-09-08 18:01:06.359443	0	2
484	6599345138	294	f	2	0	2026-09-08 18:01:18.543842	0	2
483	6599345138	364	f	2	0	2026-09-08 18:01:26.105075	0	2
530	6599345138	3948	f	1	0	2026-09-04 18:01:40.880335	0	1
481	6599345138	342	f	2	0	2026-09-08 18:01:48.028128	0	2
394	6599345138	109	f	2	0	2026-09-08 18:01:59.61694	0	2
408	6599345138	265	t	4	0	2026-10-04 01:01:24.024273	0	4
374	6599345138	224	t	4	0	2026-10-04 01:01:40.581839	0	4
379	6599345138	357	t	4	0	2026-10-19 22:13:10.138447	0	4
566	6599345138	340	f	0	0	2026-09-04 15:09:47.064113	0	1
567	6599345138	333	f	1	0	2026-09-07 15:12:17.138218	0	1
569	6599345138	362	f	1	0	2026-09-07 15:22:55.78238	0	1
561	6599345138	272	t	4	0	2026-10-06 17:02:20.602096	0	4
163	6599345138	268	t	5	2	2026-10-07 20:03:27.094466	0	4
436	6599345138	306	f	3	0	2026-09-21 20:03:42.904368	0	3
587	6599345138	316	f	0	1	2026-09-08 20:03:53.142667	0	0
589	6599345138	320	f	1	0	2026-09-10 20:04:14.604901	0	1
582	6599345138	1439	f	1	1	2026-09-10 20:04:33.696778	0	1
604	6599345138	3952	f	0	0	2026-09-19 22:26:06.428283	0	1
593	6599345138	3951	f	0	0	2026-09-07 20:27:24.485511	0	1
594	6599345138	285	f	1	0	2026-09-12 19:43:50.57356	0	1
454	6599345138	278	f	3	0	2026-09-23 19:52:45.796617	0	3
529	6599345138	3947	f	2	0	2026-09-16 19:53:03.944124	0	2
563	6599345138	313	f	2	0	2026-09-16 19:53:13.027203	0	2
392	6599345138	178	t	4	0	2026-10-23 11:49:53.087683	0	4
389	6599345138	144	f	3	0	2026-10-04 13:20:46.995972	0	3
581	6599345138	110	f	2	0	2026-09-27 13:21:06.57662	0	2
432	6599345138	293	f	3	0	2026-10-04 13:21:12.293147	0	3
401	6599345138	233	t	5	1	2026-10-20 13:33:55.232119	0	4
398	6599345138	214	t	5	0	2026-10-23 11:46:36.789777	0	4
565	6599345138	334	t	4	2	2026-10-23 11:49:23.88318	0	4
580	6599345138	165	f	2	1	2026-09-30 11:49:33.673829	0	2
406	6599345138	223	t	5	0	2026-10-20 13:20:10.054403	0	4
369	6599345138	3945	t	4	0	2026-10-20 13:20:56.007904	0	4
618	6599345138	3953	f	0	0	2026-09-23 11:48:15.808003	0	1
\.


--
-- Data for Name: words; Type: TABLE DATA; Schema: public; Owner: translaytor
--

COPY public.words (id, word, translation, language, image_url, level, category, audio_url) FROM stdin;
1	apple	яблоко	en	https://cdn.pixabay.com/photo/2016/09/29/08/33/apple-1702316_150.jpg	A1	\N	\N
91	friendship	дружба	en	https://cdn.pixabay.com/photo/2017/03/19/10/49/valentines-day-background-2156174_150.jpg	A1	people	\N
95	hero	герой	en	https://cdn.pixabay.com/photo/2016/06/03/17/35/shoes-1433925_150.jpg	A1	people	\N
102	waiter	официант	en	https://cdn.pixabay.com/photo/2016/11/21/16/02/outdoor-dining-1846137_150.jpg	A1	people	\N
71	single	одинокий/не женат	en	https://cdn.pixabay.com/photo/2021/01/29/17/17/sky-5961642_150.jpg	A1	people	\N
114	ceiling	потолок	en	https://cdn.pixabay.com/photo/2022/09/02/13/45/paris-7427636_150.jpg	A1	home	\N
121	balcony	балкон	en	https://cdn.pixabay.com/photo/2016/11/21/15/09/apartments-1845884_150.jpg	A1	home	\N
131	closet	гардероб	en	https://cdn.pixabay.com/photo/2016/11/19/13/06/bed-1839184_150.jpg	A1	home	\N
142	pen	ручка	en	https://cdn.pixabay.com/photo/2018/06/17/17/48/merry-christmas-3481061_150.jpg	A1	home	\N
146	television	телевизор	en	https://cdn.pixabay.com/photo/2021/10/30/18/03/berlin-6755246_150.jpg	A1	home	\N
8	bread	хлеб	en	https://cdn.pixabay.com/photo/2025/10/01/01/13/sourdough-9865309_150.jpg	A1	food	\N
153	sock	носок	en	https://cdn.pixabay.com/photo/2021/05/03/13/38/fairy-flower-6226285_150.jpg	A1	home	\N
9	milk	молоко	en	https://cdn.pixabay.com/photo/2014/11/05/16/35/milk-518067_150.jpg	A1	food	\N
11	cat	кот	en	https://cdn.pixabay.com/photo/2016/09/05/21/37/cat-1647775_150.jpg	A1	animals	\N
12	bird	птица	en	https://cdn.pixabay.com/photo/2025/05/04/18/04/robin-9578746_150.jpg	A1	animals	\N
161	water	вода	en	https://cdn.pixabay.com/photo/2020/06/01/08/46/water-5245722_150.jpg	A1	home	\N
13	car	машина	en	https://cdn.pixabay.com/photo/2020/05/19/10/05/opel-5190050_150.jpg	A1	transport	\N
14	bus	автобус	en	https://cdn.pixabay.com/photo/2017/09/08/23/54/bus-2730653_150.jpg	A1	transport	\N
167	open	открытый	en	https://cdn.pixabay.com/photo/2016/03/27/18/31/book-1283468_150.jpg	A1	home	\N
177	doorbell	звонок	en	https://cdn.pixabay.com/photo/2019/05/30/16/05/bell-4240100_150.jpg	A1	home	\N
184	stand	стоять	en	https://cdn.pixabay.com/photo/2022/11/08/12/56/umbel-flower-7578435_150.jpg	A1	home	\N
188	build	строить	en	https://cdn.pixabay.com/photo/2013/11/05/19/12/buildings-205986_150.jpg	A1	home	\N
197	meal	приём пищи	en	https://cdn.pixabay.com/photo/2017/06/16/18/35/tarte-2409958_150.jpg	A1	food	\N
205	meat	мясо	en	https://cdn.pixabay.com/photo/2015/03/03/22/54/meat-658029_150.jpg	A1	food	\N
214	salt	соль	en	https://cdn.pixabay.com/photo/2018/01/04/07/59/salt-harvesting-3060093_150.jpg	A1	food	\N
221	candy	конфета	en	https://cdn.pixabay.com/photo/2012/06/27/15/02/candy-50838_150.jpg	A1	food	\N
229	lemon	лимон	en	https://cdn.pixabay.com/photo/2016/01/02/01/49/lemon-1117568_150.jpg	A1	food	\N
233	strawberry	клубника	en	https://cdn.pixabay.com/photo/2022/05/27/10/35/strawberry-7224875_150.jpg	A1	food	\N
241	salad	салат	en	https://cdn.pixabay.com/photo/2021/01/10/04/37/salad-5904093_150.jpg	A1	food	\N
249	juice	сок	en	https://cdn.pixabay.com/photo/2022/07/14/06/35/smoothie-7320560_150.jpg	A1	drink	\N
375	boat	лодка	en	https://cdn.pixabay.com/photo/2016/04/05/11/04/india-1309206_150.jpg	A1	transport	\N
378	station	станция	en	https://cdn.pixabay.com/photo/2012/11/28/11/25/satellite-67718_150.jpg	A1	transport	\N
389	country	страна	en	https://cdn.pixabay.com/photo/2020/04/22/08/06/dolomites-5076487_150.jpg	A1	city	\N
397	market	рынок	en	https://cdn.pixabay.com/photo/2022/03/27/10/18/market-7094635_150.jpg	A1	places	\N
263	taste	вкус	en	https://cdn.pixabay.com/photo/2017/03/10/13/57/cooking-2132874_150.jpg	A1	food	\N
273	full	сытый	en	https://cdn.pixabay.com/photo/2018/03/02/19/21/nature-3194001_150.jpg	A1	food	\N
282	cow	корова	en	https://cdn.pixabay.com/photo/2016/10/04/23/52/cow-1715829_150.jpg	A1	animals	\N
290	rat	крыса	en	https://cdn.pixabay.com/photo/2019/12/12/22/46/animal-4691724_150.jpg	A1	animals	\N
297	monkey	обезьяна	en	https://cdn.pixabay.com/photo/2018/09/25/21/32/monkey-3703230_150.jpg	A1	animals	\N
305	panda	панда	en	https://cdn.pixabay.com/photo/2022/10/07/09/24/little-panda-7504633_150.jpg	A1	animals	\N
307	leopard	леопард	en	https://cdn.pixabay.com/photo/2013/07/16/17/12/leopard-163035_150.jpg	A1	animals	\N
315	lizard	ящерица	en	https://cdn.pixabay.com/photo/2024/11/07/03/12/lizard-9179598_150.jpg	A1	animals	\N
322	insect	насекомое	en	https://cdn.pixabay.com/photo/2012/04/01/00/45/butterfly-23063_150.jpg	A1	animals	\N
333	mouth	рот	en	https://cdn.pixabay.com/photo/2020/01/05/20/04/mouth-4743981_150.jpg	A1	animals	\N
340	feed	кормить	en	https://cdn.pixabay.com/photo/2023/04/24/15/06/great-tit-7948318_150.jpg	A1	animals	\N
353	cute	милый	en	https://cdn.pixabay.com/photo/2020/03/31/19/20/dog-4988985_150.jpg	A1	animals	\N
361	river	река	en	https://cdn.pixabay.com/photo/2019/07/14/10/48/river-4336788_150.jpg	A1	animals	\N
371	bicycle	велосипед	en	https://cdn.pixabay.com/photo/2023/04/25/16/56/bike-7950617_150.jpg	A1	transport	\N
409	church	церковь	en	https://cdn.pixabay.com/photo/2023/01/23/23/20/altar-7739897_150.jpg	A1	places	\N
412	pharmacy	аптека	en	https://cdn.pixabay.com/photo/2018/03/10/19/32/logo-pharmacy-3215049_150.jpg	A1	places	\N
419	near	рядом	en	https://cdn.pixabay.com/photo/2025/05/23/18/47/nature-9618381_150.jpg	A1	city	\N
430	stop	останавливаться	en	https://cdn.pixabay.com/photo/2019/01/30/11/52/businessman-3964425_150.jpg	A1	verbs	\N
858	lesson	урок	en	https://cdn.pixabay.com/photo/2023/10/28/10/31/child-8347081_150.jpg	A1	school	\N
871	subject	предмет	en	https://cdn.pixabay.com/photo/2019/02/25/12/01/use-4019500_150.jpg	A1	school	\N
881	worker	работник	en	https://cdn.pixabay.com/photo/2021/06/09/01/55/worker-6322085_150.jpg	A1	work	\N
899	brush	чистить	en	https://cdn.pixabay.com/photo/2020/01/05/20/02/chanel-4743979_150.jpg	A1	daily	\N
911	play	играть	en	https://cdn.pixabay.com/photo/2020/03/30/12/42/indian-4984147_150.jpg	A1	daily	\N
923	talk	говорить	en	https://cdn.pixabay.com/photo/2021/08/04/03/06/hanoi-6520941_150.jpg	A1	daily	\N
3951	вилы	pitchfork	en	\N	1	history	\N
1423	yesterday	вчера	en	https://cdn.pixabay.com/photo/2013/12/01/12/02/yesterday-221763_150.jpg	A1	time	\N
1426	evening	вечер	en	https://cdn.pixabay.com/photo/2017/01/30/16/10/sunset-2021262_150.jpg	A1	time	\N
63	aunt	тётя	en	https://cdn.pixabay.com/photo/2017/02/23/13/56/mom-and-pop-store-2092262_150.jpg	A1	people	\N
68	old	старый	en	https://cdn.pixabay.com/photo/2018/09/10/12/49/hand-3666974_150.jpg	A1	people	\N
134	light	свет	en	https://cdn.pixabay.com/photo/2017/03/19/11/07/light-2156209_150.jpg	A1	home	\N
1434	before	до	en	https://cdn.pixabay.com/photo/2020/09/03/18/12/the-akashi-kaikyo-bridge-5542079_150.jpg	A1	time	\N
1441	six	шесть	en	https://cdn.pixabay.com/photo/2010/12/13/10/01/guitar-2119_150.jpg	A1	numbers	\N
224	pizza	пицца	en	https://cdn.pixabay.com/photo/2017/12/10/14/47/pizza-3010062_150.jpg	A1	food	\N
228	orange	апельсин	en	https://cdn.pixabay.com/photo/2017/01/20/15/06/oranges-1995056_150.jpg	A1	food	\N
231	pear	груша	en	https://cdn.pixabay.com/photo/2022/08/02/17/50/pear-7360921_150.jpg	A1	food	\N
234	watermelon	арбуз	en	https://cdn.pixabay.com/photo/2014/11/30/07/16/watermelon-551235_150.jpg	A1	food	\N
236	potato	картофель	en	https://cdn.pixabay.com/photo/2018/05/29/23/18/potato-3440360_150.jpg	A1	food	\N
239	carrot	морковь	en	https://cdn.pixabay.com/photo/2015/03/14/14/00/carrots-673184_150.jpg	A1	food	\N
242	bean	фасоль	en	https://cdn.pixabay.com/photo/2023/12/15/18/07/bean-8451254_150.jpg	A1	food	\N
243	corn	кукуруза	en	https://cdn.pixabay.com/photo/2020/05/21/06/58/corn-5199393_150.jpg	A1	food	\N
247	coffee	кофе	en	https://cdn.pixabay.com/photo/2017/09/04/18/39/coffee-2714970_150.jpg	A1	drink	\N
250	drink	напиток	en	https://cdn.pixabay.com/photo/2016/03/30/19/28/coffee-break-1291381_150.jpg	A1	drink	\N
252	wine	вино	en	https://cdn.pixabay.com/photo/2017/09/26/16/44/wine-2789265_150.jpg	A1	drink	\N
257	bowl	миска	en	https://cdn.pixabay.com/photo/2016/11/21/11/57/bowl-1844894_150.jpg	A1	food	\N
259	knife	нож	en	https://cdn.pixabay.com/photo/2016/06/10/16/32/potatoes-1448405_150.jpg	A1	food	\N
262	eat	есть	en	https://cdn.pixabay.com/photo/2022/11/22/13/21/otter-7609666_150.jpg	A1	food	\N
264	sweet	сладкий	en	https://cdn.pixabay.com/photo/2016/01/02/18/39/puppy-1118584_150.jpg	A1	food	\N
268	fresh	свежий	en	https://cdn.pixabay.com/photo/2016/04/19/21/30/strawberries-1339969_150.jpg	A1	food	\N
271	hungry	голодный	en	https://cdn.pixabay.com/photo/2015/07/14/06/06/man-844208_150.jpg	A1	food	\N
274	buy	покупать	en	https://cdn.pixabay.com/photo/2025/08/27/07/33/heart-9799423_150.jpg	A1	food	\N
278	cat	кошка	en	https://cdn.pixabay.com/photo/2016/09/05/21/37/cat-1647775_150.jpg	A1	animals	\N
283	pig	свинья	en	https://cdn.pixabay.com/photo/2017/08/09/00/29/son-of-a-bitch-2613125_150.jpg	A1	animals	\N
287	duck	утка	en	https://cdn.pixabay.com/photo/2018/06/16/00/39/mallard-3478011_150.jpg	A1	animals	\N
289	mouse	мышь	en	https://cdn.pixabay.com/photo/2020/04/14/14/57/house-mouse-5043031_150.jpg	A1	animals	\N
291	frog	лягушка	en	https://cdn.pixabay.com/photo/2014/10/05/11/26/tree-frog-474949_150.jpg	A1	animals	\N
292	snake	змея	en	https://cdn.pixabay.com/photo/2023/05/09/23/47/tree-snake-7982626_150.jpg	A1	animals	\N
294	lion	лев	en	https://cdn.pixabay.com/photo/2018/04/13/21/24/lion-3317670_150.jpg	A1	animals	\N
296	elephant	слон	en	https://cdn.pixabay.com/photo/2013/05/29/22/25/elephant-114543_150.jpg	A1	animals	\N
299	wolf	волк	en	https://cdn.pixabay.com/photo/2016/04/18/10/17/wolf-1336229_150.jpg	A1	animals	\N
302	giraffe	жираф	en	https://cdn.pixabay.com/photo/2024/10/24/15/55/giraffe-9146077_150.jpg	A1	animals	\N
304	kangaroo	кенгуру	en	https://cdn.pixabay.com/photo/2021/08/19/10/47/kangaroo-6557734_150.jpg	A1	animals	\N
306	camel	верблюд	en	https://cdn.pixabay.com/photo/2023/12/04/19/45/camel-8430227_150.jpg	A1	animals	\N
309	shark	акула	en	https://cdn.pixabay.com/photo/2025/08/05/17/53/shark-9757306_150.jpg	A1	animals	\N
312	octopus	осьминог	en	https://cdn.pixabay.com/photo/2018/03/26/13/40/nature-3262715_150.jpg	A1	animals	\N
316	butterfly	бабочка	en	https://cdn.pixabay.com/photo/2015/08/05/21/22/silver-bordered-fritillary-877121_150.jpg	A1	animals	\N
318	ant	муравей	en	https://cdn.pixabay.com/photo/2020/04/19/05/33/ants-5061910_150.jpg	A1	animals	\N
321	worm	червь	en	https://cdn.pixabay.com/photo/2020/06/09/18/52/fern-5279645_150.jpg	A1	animals	\N
327	leg	нога	en	https://cdn.pixabay.com/photo/2023/12/17/10/58/spider-8453990_150.jpg	A1	animals	\N
331	ear	ухо	en	https://cdn.pixabay.com/photo/2023/06/22/04/19/rye-8080482_150.jpg	A1	animals	\N
334	tooth	зуб	en	https://cdn.pixabay.com/photo/2016/07/13/14/52/zahnreinigung-1514692_150.jpg	A1	animals	\N
335	fur	шерсть	en	https://cdn.pixabay.com/photo/2018/05/07/10/48/husky-3380548_150.jpg	A1	animals	\N
1449	fourteen	четырнадцать	en	https://cdn.pixabay.com/photo/2018/06/03/22/11/duckling-3451729_150.jpg	A1	numbers	\N
1455	second	второй	en	https://cdn.pixabay.com/photo/2016/01/27/04/32/books-1163695_150.jpg	A1	numbers	\N
1463	orange	оранжевый	en	https://cdn.pixabay.com/photo/2017/01/20/15/06/oranges-1995056_150.jpg	A1	colors	\N
1473	trousers	брюки	en	https://cdn.pixabay.com/photo/2017/11/26/19/50/jeans-2979818_150.jpg	A1	clothes	\N
1484	scarf	шарф	en	https://cdn.pixabay.com/photo/2016/04/04/21/49/woman-1308309_150.jpg	A1	clothes	\N
1487	wear	носить	en	https://cdn.pixabay.com/photo/2022/09/21/14/14/woman-7470449_150.jpg	A1	clothes	\N
2065	hand	кисть руки	en	https://cdn.pixabay.com/photo/2020/02/21/12/58/toddler-hand-4867454_150.jpg	A1	body	\N
2074	health	здоровье	en	https://cdn.pixabay.com/photo/2016/10/18/08/52/blood-pressure-monitor-1749577_150.jpg	A1	health	\N
2083	cough	кашель	en	https://cdn.pixabay.com/photo/2016/08/07/11/25/hustelinchen-1576079_150.png	A1	health	\N
2087	walk	ходить	en	https://cdn.pixabay.com/photo/2020/06/12/17/59/squirrel-5291230_150.jpg	A1	health	\N
2094	nature	природа	en	https://cdn.pixabay.com/photo/2022/04/15/07/58/sunset-7133867_150.jpg	A1	nature	\N
2105	island	остров	en	https://cdn.pixabay.com/photo/2016/03/28/09/33/island-1285147_150.jpg	A1	nature	\N
3952	ложка	spoon	en	\N	1	history	\N
2112	star	звезда	en	https://cdn.pixabay.com/photo/2011/12/14/12/17/galaxy-11098_150.jpg	A1	nature	\N
2115	sunny	солнечный	en	https://cdn.pixabay.com/photo/2019/07/22/16/13/children-4355469_150.jpg	A1	weather	\N
2124	cool	прохладный	en	https://cdn.pixabay.com/photo/2021/01/08/06/32/cafe-5899078_150.jpg	A1	weather	\N
2131	winter	зима	en	https://cdn.pixabay.com/photo/2022/12/10/11/08/trees-7646958_150.jpg	A1	weather	\N
2782	tour	тур	en	https://cdn.pixabay.com/photo/2023/02/04/16/29/boat-7767575_150.jpg	A1	travel	\N
2815	cheap	дешёвый	en	https://cdn.pixabay.com/photo/2017/07/04/10/57/kermit-2470675_150.jpg	A1	shopping	\N
2832	get	получать	en	https://cdn.pixabay.com/photo/2014/12/10/10/04/teddy-562960_150.jpg	A1	verbs	\N
2839	want	хотеть	en	https://cdn.pixabay.com/photo/2016/02/08/20/26/birds-1187581_150.jpg	A1	verbs	\N
2846	try	пробовать	en	https://cdn.pixabay.com/photo/2019/03/18/10/43/possible-4062861_150.jpg	A1	verbs	\N
3627	low	низкий	en	https://cdn.pixabay.com/photo/2020/11/14/13/29/tidal-5741708_150.jpg	A1	adjectives	\N
3651	important	важный	en	https://cdn.pixabay.com/photo/2017/12/24/21/08/secret-3037639_150.jpg	A1	adjectives	\N
3690	west	запад	en	https://cdn.pixabay.com/photo/2022/10/17/15/40/frankfurt-7528062_150.jpg	A1	city	\N
3769	pan	сковорода	en	https://cdn.pixabay.com/photo/2018/03/18/20/10/fried-3238173_150.jpg	A1	cooking	\N
3776	fry	жарить	en	https://cdn.pixabay.com/photo/2016/11/18/15/31/cooking-1835369_150.jpg	A1	cooking	\N
3795	she	она	en	https://cdn.pixabay.com/photo/2015/03/19/04/18/old-man-680382_150.jpg	A1	pronouns	\N
3810	who	кто	en	https://cdn.pixabay.com/photo/2017/06/04/19/07/who-come-after-2371910_150.jpg	A1	questions	\N
2850	speak	говорить	en	https://cdn.pixabay.com/photo/2016/03/23/13/36/frogs-1274769_150.jpg	A1	verbs	\N
3606	tired	уставший	en	https://cdn.pixabay.com/photo/2022/04/06/20/54/man-7116367_150.jpg	A1	emotions	\N
3612	love	любовь	en	https://cdn.pixabay.com/photo/2017/10/11/11/31/roses-2840743_150.jpg	A1	emotions	\N
3814	how	как	en	https://cdn.pixabay.com/photo/2015/08/26/11/06/yes-908345_150.jpg	A1	questions	\N
3828	between	между	en	https://cdn.pixabay.com/photo/2017/08/27/16/20/viet-nam-2686634_150.jpg	A1	prepositions	\N
3843	good night	спокойной ночи	en	https://cdn.pixabay.com/photo/2016/05/23/17/09/moon-1410779_150.jpg	A1	phrases	\N
3849	I understand	я понимаю	en	https://cdn.pixabay.com/photo/2016/04/14/00/42/sisters-1328070_150.jpg	A1	phrases	\N
16	man	мужчина	en	https://cdn.pixabay.com/photo/2016/11/21/12/42/beard-1845166_150.jpg	A1	people	\N
17	woman	женщина	en	https://cdn.pixabay.com/photo/2017/11/19/07/30/girl-2961959_150.jpg	A1	people	\N
20	child	ребёнок	en	https://cdn.pixabay.com/photo/2014/01/04/13/21/toddler-238466_150.jpg	A1	people	\N
22	father	отец	en	https://cdn.pixabay.com/photo/2016/11/14/04/45/bicycle-1822640_150.jpg	A1	people	\N
25	daughter	дочь	en	https://cdn.pixabay.com/photo/2021/08/27/10/16/baby-6578335_150.jpg	A1	people	\N
28	family	семья	en	https://cdn.pixabay.com/photo/2017/08/08/03/50/family-2610205_150.jpg	A1	people	\N
31	people	люди	en	https://cdn.pixabay.com/photo/2021/08/14/18/01/people-6545894_150.jpg	A1	people	\N
35	husband	муж	en	https://cdn.pixabay.com/photo/2019/05/24/18/41/marriage-4226896_150.jpg	A1	people	\N
37	student	ученик	en	https://cdn.pixabay.com/photo/2017/02/27/23/34/college-2104580_150.jpg	A1	people	\N
39	nurse	медсестра	en	https://cdn.pixabay.com/photo/2017/01/29/21/16/nurse-2019420_150.jpg	A1	people	\N
42	farmer	фермер	en	https://cdn.pixabay.com/photo/2020/03/15/13/19/lotus-flowers-4933604_150.jpg	A1	people	\N
45	boss	начальник	en	https://cdn.pixabay.com/photo/2015/05/04/19/48/gorilla-752875_150.jpg	A1	people	\N
49	customer	клиент	en	https://cdn.pixabay.com/photo/2018/12/09/12/29/customer-3864809_150.jpg	A1	people	\N
52	classmate	одноклассник	en	https://cdn.pixabay.com/photo/2014/07/06/09/37/lecture-385357_150.jpg	A1	people	\N
55	king	король	en	https://cdn.pixabay.com/photo/2023/10/27/10/49/australian-king-parrot-8345064_150.jpg	A1	people	\N
58	girlfriend	девушка	en	https://cdn.pixabay.com/photo/2018/11/06/14/01/happy-valentines-day-3798371_150.jpg	A1	people	\N
61	grandmother	бабушка	en	https://cdn.pixabay.com/photo/2013/04/04/06/42/woman-100342_150.jpg	A1	people	\N
3913	hot	жарко	en	https://cdn.pixabay.com/photo/2020/09/21/05/57/coffee-5589036_150.jpg	A1	weather	\N
2	dog	собака	en	https://cdn.pixabay.com/photo/2016/01/05/17/51/maltese-1123016_150.jpg	A1	\N	\N
65	relative	родственник	en	https://cdn.pixabay.com/photo/2016/06/28/02/15/retro-1483781_150.jpg	A1	people	\N
67	teenager	подросток	en	https://cdn.pixabay.com/photo/2016/11/14/05/29/girl-1822702_150.jpg	A1	people	\N
69	young	молодой	en	https://cdn.pixabay.com/photo/2014/12/19/17/22/chicks-573377_150.jpg	A1	people	\N
338	farm	ферма	en	https://cdn.pixabay.com/photo/2017/10/29/15/58/trees-2900064_150.jpg	A1	animals	\N
73	poor	бедный	en	https://cdn.pixabay.com/photo/2017/07/10/09/24/poor-2489481_150.jpg	A1	people	\N
74	happy	счастливый	en	https://cdn.pixabay.com/photo/2017/08/02/23/58/people-2574170_150.jpg	A1	people	\N
76	kind	добрый	en	https://cdn.pixabay.com/photo/2023/08/02/12/39/bird-8165143_150.jpg	A1	people	\N
79	strong	сильный	en	https://cdn.pixabay.com/photo/2020/06/15/16/05/animal-5302420_150.jpg	A1	people	\N
82	short	низкий	en	https://cdn.pixabay.com/photo/2026/02/14/17/57/veronika_andrews-short-eared-owl-10123513_150.jpg	A1	people	\N
85	silly	глупый	en	https://cdn.pixabay.com/photo/2015/04/27/22/53/man-742766_150.jpg	A1	people	\N
92	team	команда	en	https://cdn.pixabay.com/photo/2020/07/08/04/12/work-5382501_150.jpg	A1	people	\N
93	group	группа	en	https://cdn.pixabay.com/photo/2023/01/26/18/09/zebra-7746719_150.jpg	A1	people	\N
96	artist	художник	en	https://cdn.pixabay.com/photo/2020/12/22/16/30/art-5852645_150.jpg	A1	people	\N
99	writer	писатель	en	https://cdn.pixabay.com/photo/2024/03/09/16/59/typewriter-8622984_150.jpg	A1	people	\N
101	seller	продавец	en	https://cdn.pixabay.com/photo/2022/11/15/10/10/fruit-seller-7593634_150.jpg	A1	people	\N
104	engineer	инженер	en	https://cdn.pixabay.com/photo/2024/01/10/16/22/man-8499961_150.jpg	A1	people	\N
70	married	женатый/замужем	en	https://cdn.pixabay.com/photo/2016/01/01/16/38/wedding-night-1116722_150.jpg	A1	people	\N
107	home	дом/жильё	en	https://cdn.pixabay.com/photo/2017/07/09/03/19/home-2486092_150.jpg	A1	home	\N
110	window	окно	en	https://cdn.pixabay.com/photo/2022/10/24/07/11/window-7542846_150.jpg	A1	home	\N
111	wall	стена	en	https://cdn.pixabay.com/photo/2016/12/18/21/23/brick-wall-1916752_150.jpg	A1	home	\N
113	roof	крыша	en	https://cdn.pixabay.com/photo/2024/08/28/14/04/roof-9004113_150.jpg	A1	home	\N
116	kitchen	кухня	en	https://cdn.pixabay.com/photo/2017/03/22/17/39/kitchen-2165756_150.jpg	A1	home	\N
119	living room	гостиная	en	https://cdn.pixabay.com/photo/2016/11/30/08/48/bedroom-1872196_150.jpg	A1	home	\N
122	stairs	лестница	en	https://cdn.pixabay.com/photo/2020/01/20/22/21/palace-4781577_150.jpg	A1	home	\N
341	walk	гулять	en	https://cdn.pixabay.com/photo/2020/06/12/17/59/squirrel-5291230_150.jpg	A1	animals	\N
343	jump	прыгать	en	https://cdn.pixabay.com/photo/2021/11/09/08/23/skate-6781021_150.jpg	A1	animals	\N
351	dangerous	опасный	en	https://cdn.pixabay.com/photo/2017/01/11/20/03/wolf-1972762_150.jpg	A1	animals	\N
356	baby	детёныш	en	https://cdn.pixabay.com/photo/2023/06/11/14/38/baby-8056153_150.jpg	A1	animals	\N
359	home	дом	en	https://cdn.pixabay.com/photo/2017/07/09/03/19/home-2486092_150.jpg	A1	animals	\N
360	forest	лес	en	https://cdn.pixabay.com/photo/2015/06/19/21/24/avenue-815297_150.jpg	A1	animals	\N
363	tree	дерево	en	https://cdn.pixabay.com/photo/2016/12/27/21/03/lone-tree-1934897_150.jpg	A1	animals	\N
369	plane	самолёт	en	https://cdn.pixabay.com/photo/2019/11/03/09/35/cockpit-4598188_150.jpg	A1	transport	\N
372	motorcycle	мотоцикл	en	https://cdn.pixabay.com/photo/2016/11/29/10/21/dirt-bike-1868996_150.jpg	A1	transport	\N
374	truck	грузовик	en	https://cdn.pixabay.com/photo/2019/12/01/20/07/truck-4666300_150.jpg	A1	transport	\N
377	subway	метро	en	https://cdn.pixabay.com/photo/2024/10/26/11/15/subway-9151034_150.jpg	A1	transport	\N
380	road	дорога	en	https://cdn.pixabay.com/photo/2014/01/04/12/34/road-238458_150.jpg	A1	transport	\N
383	traffic	движение транспорта	en	https://cdn.pixabay.com/photo/2022/05/22/11/10/highway-7213206_150.jpg	A1	city	\N
386	city	город	en	https://cdn.pixabay.com/photo/2023/08/04/22/59/sunset-8170058_150.jpg	A1	city	\N
388	village	деревня	en	https://cdn.pixabay.com/photo/2022/06/12/22/35/village-7258991_150.jpg	A1	city	\N
390	capital	столица	en	https://cdn.pixabay.com/photo/2020/01/30/12/27/st-petersburg-4805295_150.jpg	A1	city	\N
394	hospital	больница	en	https://cdn.pixabay.com/photo/2016/11/08/05/29/operation-1807543_150.jpg	A1	places	\N
396	shop	магазин	en	https://cdn.pixabay.com/photo/2016/11/22/21/57/apparel-1850804_150.jpg	A1	places	\N
399	cafe	кафе	en	https://cdn.pixabay.com/photo/2021/01/08/06/32/cafe-5899078_150.jpg	A1	places	\N
401	park	парк	en	https://cdn.pixabay.com/photo/2018/03/15/21/10/tree-3229512_150.jpg	A1	places	\N
403	museum	музей	en	https://cdn.pixabay.com/photo/2016/09/06/18/22/visitors-1649815_150.jpg	A1	places	\N
406	company	компания	en	https://cdn.pixabay.com/photo/2021/03/29/12/16/stairs-6133971_150.jpg	A1	work	\N
410	store	магазин	en	https://cdn.pixabay.com/photo/2016/03/02/20/13/grocery-1232944_150.jpg	A1	places	\N
411	supermarket	супермаркет	en	https://cdn.pixabay.com/photo/2016/03/02/20/13/grocery-1232944_150.jpg	A1	places	\N
414	police station	полицейский участок	en	https://cdn.pixabay.com/photo/2019/11/25/18/24/kingstown-4652734_150.jpg	A1	places	\N
418	straight	прямо	en	https://cdn.pixabay.com/photo/2017/06/24/23/03/railway-2439189_150.jpg	A1	city	\N
421	inside	внутри	en	https://cdn.pixabay.com/photo/2019/11/30/16/13/berlin-4663539_150.jpg	A1	city	\N
422	outside	снаружи	en	https://cdn.pixabay.com/photo/2021/01/08/06/32/cafe-5899078_150.jpg	A1	city	\N
425	where	где	en	https://cdn.pixabay.com/photo/2017/03/24/23/15/bison-2172392_150.jpg	A1	city	\N
428	drive	водить	en	https://cdn.pixabay.com/photo/2021/10/19/13/51/tunnel-6723643_150.jpg	A1	verbs	\N
431	start	начинать	en	https://cdn.pixabay.com/photo/2016/11/19/17/20/athlete-1840437_150.jpg	A1	verbs	\N
434	arrive	прибывать	en	https://cdn.pixabay.com/photo/2013/10/17/14/38/railway-station-197035_150.jpg	A1	verbs	\N
857	class	класс	en	https://cdn.pixabay.com/photo/2017/02/27/23/34/college-2104580_150.jpg	A1	school	\N
862	notebook	тетрадь	en	https://cdn.pixabay.com/photo/2017/05/12/08/29/coffee-2306471_150.jpg	A1	school	\N
868	test	тест	en	https://cdn.pixabay.com/photo/2021/08/02/18/11/covid-6517476_150.jpg	A1	school	\N
870	homework	домашняя работа	en	https://cdn.pixabay.com/photo/2018/01/17/07/06/laptop-3087585_150.jpg	A1	school	\N
873	English	английский язык	en	https://cdn.pixabay.com/photo/2022/09/24/16/32/bulldog-7476727_150.jpg	A1	school	\N
77	nice	приятный	en	https://cdn.pixabay.com/photo/2020/10/06/05/31/woman-5631257_150.jpg	A1	people	\N
124	chair	стул	en	https://cdn.pixabay.com/photo/2016/11/21/13/08/woman-1845311_150.jpg	A1	home	\N
125	bed	кровать	en	https://cdn.pixabay.com/photo/2020/11/24/11/36/bedroom-5772286_150.jpg	A1	home	\N
128	shelf	полка	en	https://cdn.pixabay.com/photo/2014/09/05/18/32/old-books-436498_150.jpg	A1	home	\N
130	cupboard	шкаф	en	https://cdn.pixabay.com/photo/2016/11/30/08/48/bedroom-1872196_150.jpg	A1	home	\N
133	lamp	лампа	en	https://cdn.pixabay.com/photo/2017/10/30/23/34/lamp-2903830_150.jpg	A1	home	\N
136	lock	замок	en	https://cdn.pixabay.com/photo/2024/04/18/19/04/lock-8704819_150.jpg	A1	home	\N
137	clock	часы	en	https://cdn.pixabay.com/photo/2017/03/26/12/36/alarm-clock-2175382_150.jpg	A1	home	\N
140	book	книга	en	https://cdn.pixabay.com/photo/2014/09/05/18/32/old-books-436498_150.jpg	A1	home	\N
143	pencil	карандаш	en	https://cdn.pixabay.com/photo/2025/03/21/18/04/art-9485478_150.jpg	A1	home	\N
145	phone	телефон	en	https://cdn.pixabay.com/photo/2016/11/22/23/40/hands-1851218_150.jpg	A1	home	\N
148	camera	камера	en	https://cdn.pixabay.com/photo/2014/08/29/14/53/camera-431119_150.jpg	A1	home	\N
151	shirt	рубашка	en	https://cdn.pixabay.com/photo/2016/11/23/00/57/adult-1851571_150.jpg	A1	home	\N
152	shoe	обувь	en	https://cdn.pixabay.com/photo/2014/06/18/18/42/running-shoe-371625_150.jpg	A1	home	\N
155	hat	шапка	en	https://cdn.pixabay.com/photo/2022/06/22/16/00/cap-7278216_150.jpg	A1	home	\N
158	brush	щётка	en	https://cdn.pixabay.com/photo/2020/01/05/20/02/chanel-4743979_150.jpg	A1	home	\N
159	toothbrush	зубная щётка	en	https://cdn.pixabay.com/photo/2018/03/01/16/43/toothbrush-3191097_150.jpg	A1	home	\N
163	shower	душ	en	https://cdn.pixabay.com/photo/2018/08/16/21/21/water-jet-3611518_150.jpg	A1	home	\N
165	clean	чистый	en	https://cdn.pixabay.com/photo/2017/02/14/18/28/fruhjahrsputz-2066605_150.jpg	A1	home	\N
168	closed	закрытый	en	https://cdn.pixabay.com/photo/2023/01/22/14/47/love-7736559_150.jpg	A1	home	\N
170	small	маленький	en	https://cdn.pixabay.com/photo/2017/09/05/11/37/baby-2717347_150.jpg	A1	home	\N
174	cold	холодный	en	https://cdn.pixabay.com/photo/2024/12/31/23/46/bridge-9302956_150.jpg	A1	home	\N
178	housework	домашняя работа	en	https://cdn.pixabay.com/photo/2014/11/15/20/30/kitchen-scale-532651_150.jpg	A1	home	\N
181	clean	убирать	en	https://cdn.pixabay.com/photo/2017/02/14/18/28/fruhjahrsputz-2066605_150.jpg	A1	home	\N
183	sit	сидеть	en	https://cdn.pixabay.com/photo/2016/11/23/15/31/man-1853545_150.jpg	A1	home	\N
186	move	двигаться	en	https://cdn.pixabay.com/photo/2020/06/28/10/02/clouds-5348740_150.jpg	A1	home	\N
187	stay	оставаться	en	https://cdn.pixabay.com/photo/2015/03/22/14/25/feet-684683_150.jpg	A1	home	\N
190	paint	красить	en	https://cdn.pixabay.com/photo/2022/01/24/13/05/hearts-6963368_150.jpg	A1	home	\N
195	glass	стакан	en	https://cdn.pixabay.com/photo/2015/10/24/11/09/red-wine-1004255_150.jpg	A1	home	\N
198	breakfast	завтрак	en	https://cdn.pixabay.com/photo/2016/11/06/23/16/breakfast-1804436_150.jpg	A1	food	\N
202	rice	рис	en	https://cdn.pixabay.com/photo/2020/09/13/16/16/terraces-5568679_150.jpg	A1	food	\N
204	soup	суп	en	https://cdn.pixabay.com/photo/2015/02/03/16/31/soup-622737_150.jpg	A1	food	\N
207	fish	рыба	en	https://cdn.pixabay.com/photo/2020/10/12/20/57/aquarium-5650174_150.jpg	A1	food	\N
208	egg	яйцо	en	https://cdn.pixabay.com/photo/2022/07/26/13/55/egg-7345934_150.jpg	A1	food	\N
212	yogurt	йогурт	en	https://cdn.pixabay.com/photo/2016/06/07/17/15/yogurt-1442034_150.jpg	A1	food	\N
215	sugar	сахар	en	https://cdn.pixabay.com/photo/2020/04/13/22/55/sugar-5040276_150.jpg	A1	food	\N
216	pepper	перец	en	https://cdn.pixabay.com/photo/2014/12/15/13/40/bell-pepper-569070_150.jpg	A1	food	\N
219	cookie	печенье	en	https://cdn.pixabay.com/photo/2017/11/24/20/01/christmas-cookies-2975570_150.jpg	A1	food	\N
222	ice cream	мороженое	en	https://cdn.pixabay.com/photo/2016/08/18/00/37/ice-1601932_150.jpg	A1	food	\N
876	work	работа	en	https://cdn.pixabay.com/photo/2015/01/08/18/26/man-593333_150.jpg	A1	work	\N
893	money	деньги	en	https://cdn.pixabay.com/photo/2017/03/27/21/31/money-2180330_150.jpg	A1	work	\N
896	wake up	просыпаться	en	https://cdn.pixabay.com/photo/2017/03/04/13/12/new-year-2116007_150.jpg	A1	daily	\N
900	dress	одеваться	en	https://cdn.pixabay.com/photo/2021/04/16/07/22/ao-dai-6182834_150.jpg	A1	daily	\N
908	write	писать	en	https://cdn.pixabay.com/photo/2024/03/09/16/59/typewriter-8622984_150.jpg	A1	daily	\N
910	watch	смотреть	en	https://cdn.pixabay.com/photo/2014/12/08/14/23/pocket-watch-560937_150.jpg	A1	daily	\N
916	open	открывать	en	https://cdn.pixabay.com/photo/2016/03/27/18/31/book-1283468_150.jpg	A1	daily	\N
919	finish	заканчивать	en	https://cdn.pixabay.com/photo/2019/09/21/06/57/p38-4493176_150.jpg	A1	daily	\N
922	meet	встречать	en	https://cdn.pixabay.com/photo/2017/08/07/18/28/businessman-2606509_150.jpg	A1	daily	\N
1416	time	время	en	https://cdn.pixabay.com/photo/2017/03/26/12/36/alarm-clock-2175382_150.jpg	A1	time	\N
1417	day	день	en	https://cdn.pixabay.com/photo/2023/01/13/05/06/doomsday-style-7715286_150.jpg	A1	time	\N
1418	week	неделя	en	https://cdn.pixabay.com/photo/2025/12/31/14/04/calendar-10045176_150.jpg	A1	time	\N
1421	today	сегодня	en	https://cdn.pixabay.com/photo/2015/07/06/11/38/shrimp-salad-833214_150.jpg	A1	time	\N
1424	morning	утро	en	https://cdn.pixabay.com/photo/2018/03/08/09/10/dawn-3208158_150.jpg	A1	time	\N
1427	night	ночь	en	https://cdn.pixabay.com/photo/2020/04/30/20/14/sky-5114501_150.jpg	A1	time	\N
1429	minute	минута	en	https://cdn.pixabay.com/photo/2016/02/17/09/20/watches-1204696_150.jpg	A1	time	\N
1431	early	рано	en	https://cdn.pixabay.com/photo/2023/01/14/13/17/bellflower-7718193_150.jpg	A1	time	\N
1433	now	сейчас	en	https://cdn.pixabay.com/photo/2017/06/07/12/41/sunrise-2380255_150.jpg	A1	time	\N
1436	one	один	en	https://cdn.pixabay.com/photo/2016/11/21/17/40/buildings-1846728_150.jpg	A1	numbers	\N
1439	four	четыре	en	https://cdn.pixabay.com/photo/2017/01/03/16/54/klee-1949981_150.jpg	A1	numbers	\N
80	weak	слабый	en	https://cdn.pixabay.com/photo/2015/06/17/11/08/caricature-812270_150.jpg	A1	people	\N
84	smart	умный	en	https://cdn.pixabay.com/photo/2019/09/02/15/43/smarthome-4447519_150.jpg	A1	people	\N
1440	five	пять	en	https://cdn.pixabay.com/photo/2018/03/22/22/43/cocktails-3252160_150.jpg	A1	numbers	\N
1443	eight	восемь	en	https://cdn.pixabay.com/photo/2016/10/26/22/05/spider-1772769_150.jpg	A1	numbers	\N
1446	eleven	одиннадцать	en	https://cdn.pixabay.com/photo/2014/09/07/15/39/number-437929_150.jpg	A1	numbers	\N
1448	thirteen	тринадцать	en	https://cdn.pixabay.com/photo/2016/08/11/22/12/door-1587023_150.jpg	A1	numbers	\N
1451	twenty	двадцать	en	https://cdn.pixabay.com/photo/2016/04/25/23/53/euro-1353420_150.jpg	A1	numbers	\N
1454	first	первый	en	https://cdn.pixabay.com/photo/2015/09/01/00/11/robot-916284_150.jpg	A1	numbers	\N
1457	red	красный	en	https://cdn.pixabay.com/photo/2018/01/28/08/12/nature-3112997_150.jpg	A1	colors	\N
1458	blue	синий	en	https://cdn.pixabay.com/photo/2016/11/19/18/57/godafoss-1840758_150.jpg	A1	colors	\N
1461	black	чёрный	en	https://cdn.pixabay.com/photo/2018/02/21/05/17/cat-3169476_150.jpg	A1	colors	\N
1464	pink	розовый	en	https://cdn.pixabay.com/photo/2019/05/01/09/54/pink-4170404_150.jpg	A1	colors	\N
1466	gray	серый	en	https://cdn.pixabay.com/photo/2016/11/22/20/04/abstract-1850424_150.jpg	A1	colors	\N
1469	light	светлый	en	https://cdn.pixabay.com/photo/2017/03/19/11/07/light-2156209_150.jpg	A1	colors	\N
1474	jeans	джинсы	en	https://cdn.pixabay.com/photo/2017/03/20/20/36/blue-jeans-2160265_150.jpg	A1	clothes	\N
1475	dress	платье	en	https://cdn.pixabay.com/photo/2021/04/16/07/22/ao-dai-6182834_150.jpg	A1	clothes	\N
1479	shoe	ботинок	en	https://cdn.pixabay.com/photo/2014/06/18/18/42/running-shoe-371625_150.jpg	A1	clothes	\N
1483	glove	перчатка	en	https://cdn.pixabay.com/photo/2023/10/10/17/28/wildlife-park-8306984_150.jpg	A1	clothes	\N
1486	pocket	карман	en	https://cdn.pixabay.com/photo/2014/02/01/17/50/money-256281_150.jpg	A1	clothes	\N
1489	take off	снять	en	https://cdn.pixabay.com/photo/2025/06/26/09/53/australian-pelican-9681595_150.jpg	A1	clothes	\N
2063	neck	шея	en	https://cdn.pixabay.com/photo/2019/07/27/06/21/giraffe-4366005_150.jpg	A1	body	\N
2066	finger	палец	en	https://cdn.pixabay.com/photo/2022/12/26/17/05/hands-7679387_150.jpg	A1	body	\N
2069	back	спина	en	https://cdn.pixabay.com/photo/2016/11/18/14/15/forest-1834831_150.jpg	A1	body	\N
2072	blood	кровь	en	https://cdn.pixabay.com/photo/2020/11/14/13/06/virus-5741636_150.jpg	A1	body	\N
2073	bone	кость	en	https://cdn.pixabay.com/photo/2020/10/20/22/10/skull-5671571_150.jpg	A1	body	\N
2076	healthy	здоровый	en	https://cdn.pixabay.com/photo/2022/07/14/06/35/smoothie-7320560_150.jpg	A1	health	\N
2081	fever	температура	en	https://cdn.pixabay.com/photo/2016/07/24/21/01/thermometer-1539191_150.jpg	A1	health	\N
2084	sleep	сон	en	https://cdn.pixabay.com/photo/2017/04/03/10/42/woman-2197947_150.jpg	A1	health	\N
2086	exercise	упражнение	en	https://cdn.pixabay.com/photo/2019/05/18/14/42/jogging-4211946_150.jpg	A1	health	\N
2092	help	помощь	en	https://cdn.pixabay.com/photo/2020/05/24/23/44/hands-5216585_150.jpg	A1	health	\N
2093	emergency	чрезвычайная ситуация	en	https://cdn.pixabay.com/photo/2021/11/24/03/19/firetruck-6820125_150.jpg	A1	health	\N
2103	mountain	гора	en	https://cdn.pixabay.com/photo/2024/02/12/16/05/siguniang-mountain-8568913_150.jpg	A1	nature	\N
2106	stone	камень	en	https://cdn.pixabay.com/photo/2020/10/23/06/34/stones-5677828_150.jpg	A1	nature	\N
2109	sky	небо	en	https://cdn.pixabay.com/photo/2017/09/18/15/38/moon-2762111_150.jpg	A1	nature	\N
2111	moon	луна	en	https://cdn.pixabay.com/photo/2018/03/02/19/21/nature-3194001_150.jpg	A1	nature	\N
2113	fire	огонь	en	https://cdn.pixabay.com/photo/2023/06/22/16/34/campfire-8081877_150.jpg	A1	nature	\N
2116	rain	дождь	en	https://cdn.pixabay.com/photo/2022/05/28/13/02/plant-7227222_150.jpg	A1	weather	\N
2118	wind	ветер	en	https://cdn.pixabay.com/photo/2016/09/26/17/11/wind-sock-1696481_150.jpg	A1	weather	\N
2121	hot	жаркий	en	https://cdn.pixabay.com/photo/2020/09/21/05/57/coffee-5589036_150.jpg	A1	weather	\N
2125	dry	сухой	en	https://cdn.pixabay.com/photo/2022/11/15/08/40/dry-plant-7593485_150.jpg	A1	weather	\N
2126	wet	мокрый	en	https://cdn.pixabay.com/photo/2023/11/09/01/25/road-8376079_150.png	A1	weather	\N
2129	summer	лето	en	https://cdn.pixabay.com/photo/2022/06/22/16/00/cap-7278216_150.jpg	A1	weather	\N
2132	temperature	температура	en	https://cdn.pixabay.com/photo/2018/01/20/14/07/technology-3094663_150.jpg	A1	weather	\N
2779	trip	поездка	en	https://cdn.pixabay.com/photo/2021/11/16/06/27/luggage-6800246_150.jpg	A1	travel	\N
2781	vacation	каникулы	en	https://cdn.pixabay.com/photo/2016/04/30/08/35/aircraft-1362587_150.jpg	A1	travel	\N
2805	ride	ехать	en	https://cdn.pixabay.com/photo/2022/01/09/10/28/ferris-wheel-6925693_150.jpg	A1	transport	\N
2813	price	цена	en	https://cdn.pixabay.com/photo/2020/03/15/13/59/sea-4933717_150.jpg	A1	shopping	\N
2814	cost	стоимость	en	https://cdn.pixabay.com/photo/2020/06/05/16/53/zucchini-5263781_150.jpg	A1	shopping	\N
2824	size	размер	en	https://cdn.pixabay.com/photo/2016/01/20/11/24/crochet-1151378_150.jpg	A1	shopping	\N
2826	large	большой	en	https://cdn.pixabay.com/photo/2015/08/22/15/39/giraffes-901009_150.jpg	A1	shopping	\N
2831	make	делать/создавать	en	https://cdn.pixabay.com/photo/2015/06/28/14/10/soap-bubble-824558_150.jpg	A1	verbs	\N
2834	take	брать	en	https://cdn.pixabay.com/photo/2025/06/26/09/53/australian-pelican-9681595_150.jpg	A1	verbs	\N
2837	know	знать	en	https://cdn.pixabay.com/photo/2016/10/22/02/34/bookshop-1759619_150.jpg	A1	verbs	\N
2840	need	нуждаться	en	https://cdn.pixabay.com/photo/2017/04/21/09/38/street-2248101_150.jpg	A1	verbs	\N
2843	hate	ненавидеть	en	https://cdn.pixabay.com/photo/2022/04/25/06/35/portrait-7155206_150.jpg	A1	verbs	\N
2845	use	использовать	en	https://cdn.pixabay.com/photo/2018/01/24/13/38/nun-3103950_150.jpg	A1	verbs	\N
3802	her	её	en	https://cdn.pixabay.com/photo/2018/09/18/20/55/lemur-3687245_150.jpg	A1	pronouns	\N
3805	this	это	en	https://cdn.pixabay.com/photo/2017/09/06/09/32/tortoise-2720808_150.jpg	A1	pronouns	\N
3812	when	когда	en	https://cdn.pixabay.com/photo/2020/05/31/22/11/stir-5244456_150.jpg	A1	questions	\N
3816	whose	чей	en	https://cdn.pixabay.com/photo/2016/09/14/20/01/whose-1670261_150.jpg	A1	questions	\N
3823	without	без	en	https://cdn.pixabay.com/photo/2017/08/12/22/12/bugnes-2635518_150.jpg	A1	prepositions	\N
3824	for	для	en	https://cdn.pixabay.com/photo/2016/10/27/22/59/cucumbers-1776752_150.jpg	A1	prepositions	\N
3827	over	над	en	https://cdn.pixabay.com/photo/2023/03/14/22/07/child-7853252_150.jpg	A1	prepositions	\N
3831	front	перед	en	https://cdn.pixabay.com/photo/2022/01/06/16/49/bench-6919896_150.jpg	A1	prepositions	\N
19	girl	девочка	en	https://cdn.pixabay.com/photo/2017/11/19/07/30/girl-2961959_150.jpg	A1	people	\N
23	mother	мать	en	https://cdn.pixabay.com/photo/2022/04/05/19/34/motherhood-7114294_150.jpg	A1	people	\N
3937	Tatar	татарин	en	\N	1	history	\N
3950	вилка	fork	en	\N	1	history	\N
26	brother	брат	en	https://cdn.pixabay.com/photo/2015/06/22/08/38/siblings-817369_150.jpg	A1	people	\N
3938	tray	поднос	en	\N	1	history	\N
3939	carpet	ковёр	en	\N	1	history	\N
30	person	человек	en	https://cdn.pixabay.com/photo/2014/10/16/20/00/woman-491623_150.jpg	A1	people	\N
32	name	имя	en	https://cdn.pixabay.com/photo/2016/12/15/19/45/city-1909892_150.jpg	A1	people	\N
3940	jackal	шакал	en	\N	1	history	\N
38	doctor	врач	en	https://cdn.pixabay.com/photo/2015/02/26/15/40/doctor-650534_150.jpg	A1	people	\N
40	driver	водитель	en	https://cdn.pixabay.com/photo/2016/07/04/20/10/accident-1497298_150.jpg	A1	people	\N
44	police	полиция	en	https://cdn.pixabay.com/photo/2015/10/13/12/51/policewoman-986047_150.jpg	A1	people	\N
3941	bomb	бомба	en	\N	1	history	\N
48	guest	гость	en	https://cdn.pixabay.com/photo/2016/04/26/08/00/wedding-1353829_150.jpg	A1	people	\N
330	eye	глаз	en	https://cdn.pixabay.com/photo/2016/02/01/16/10/eye-1173863_150.jpg	A1	animals	\N
3942	special forces	спецназ	en	\N	1	history	\N
3943	tablecloth	скатерть	en	\N	1	history	\N
53	partner	партнёр	en	https://cdn.pixabay.com/photo/2016/11/08/05/20/sunset-1807524_150.jpg	A1	people	\N
3944	hippopotamus	бегемот	en	\N	1	history	\N
3945	jug	кувшин	en	\N	1	history	\N
2054	body	тело	en	https://cdn.pixabay.com/photo/2017/08/07/23/25/woman-2609115_150.jpg	A1	body	\N
3946	passion fruit	маракуйя	en	\N	1	history	\N
3947	processor	процессор	en	\N	1	history	\N
3948	Masha	маша	en	\N	1	history	\N
56	queen	королева	en	https://cdn.pixabay.com/photo/2017/09/08/20/29/chess-2730034_150.jpg	A1	people	\N
60	grandfather	дедушка	en	https://cdn.pixabay.com/photo/2023/06/13/10/09/man-8060589_150.jpg	A1	people	\N
3949	board	доска	en	\N	1	history	\N
3834	goodbye	до свидания	en	https://cdn.pixabay.com/photo/2016/05/09/17/24/girl-1381989_150.jpg	A1	phrases	\N
3835	please	пожалуйста	en	https://cdn.pixabay.com/photo/2017/08/30/17/26/please-2697951_150.jpg	A1	phrases	\N
3837	sorry	извините	en	https://cdn.pixabay.com/photo/2015/01/16/08/41/dog-601216_150.jpg	A1	phrases	\N
3838	yes	да	en	https://cdn.pixabay.com/photo/2017/09/27/11/41/co-2791802_150.jpg	A1	phrases	\N
3840	okay	хорошо	en	https://cdn.pixabay.com/photo/2025/12/26/15/41/gesture-10036320_150.jpg	A1	phrases	\N
3841	welcome	добро пожаловать	en	https://cdn.pixabay.com/photo/2016/02/17/21/09/welcome-to-our-home-1205888_150.jpg	A1	phrases	\N
3842	good morning	доброе утро	en	https://cdn.pixabay.com/photo/2022/04/08/06/33/field-7118838_150.jpg	A1	phrases	\N
3844	see you	увидимся	en	https://cdn.pixabay.com/photo/2014/11/30/18/48/father-551921_150.jpg	A1	phrases	\N
3845	my name is	меня зовут	en	https://cdn.pixabay.com/photo/2021/12/28/21/23/decoration-6900215_150.jpg	A1	phrases	\N
3847	I am fine	у меня всё хорошо	en	https://cdn.pixabay.com/photo/2018/01/30/03/07/women-3117831_150.jpg	A1	phrases	\N
3848	I don't know	я не знаю	en	https://cdn.pixabay.com/photo/2020/06/28/14/35/wild-yellow-flower-5349487_150.jpg	A1	phrases	\N
3850	I need help	мне нужна помощь	en	https://cdn.pixabay.com/photo/2017/04/21/09/38/street-2248101_150.jpg	A1	phrases	\N
3851	thank you	спасибо	en	https://cdn.pixabay.com/photo/2020/04/22/11/59/thank-you-5077738_150.jpg	A1	phrases	\N
3896	pants	брюки	en	https://cdn.pixabay.com/photo/2017/11/26/19/50/jeans-2979818_150.jpg	A1	clothes	\N
3914	cold	холодно	en	https://cdn.pixabay.com/photo/2024/12/31/23/46/bridge-9302956_150.jpg	A1	weather	\N
3915	warm	тепло	en	https://cdn.pixabay.com/photo/2022/06/29/08/26/pour-7291236_150.jpg	A1	weather	\N
3921	say	говорить	en	https://cdn.pixabay.com/photo/2014/01/04/13/38/tin-can-238488_150.jpg	A1	verbs	\N
3923	make	делать	en	https://cdn.pixabay.com/photo/2015/06/28/14/10/soap-bubble-824558_150.jpg	A1	verbs	\N
3928	put	класть	en	https://cdn.pixabay.com/photo/2016/03/31/04/50/blush-1292054_150.jpg	A1	verbs	\N
3807	these	эти	en	\N	A1	pronouns	\N
3808	those	те	en	\N	A1	pronouns	\N
3822	with	с	en	\N	A1	prepositions	\N
3806	that	то	en	\N	A1	pronouns	\N
426	go	идти	en	\N	A1	verbs	\N
98	singer	певец	en	https://cdn.pixabay.com/photo/2019/10/25/18/09/music-4577592_150.jpg	A1	people	\N
105	programmer	программист	en	https://cdn.pixabay.com/photo/2016/11/19/14/00/code-1839406_150.jpg	A1	people	\N
109	door	дверь	en	https://cdn.pixabay.com/photo/2024/05/27/13/34/door-8791308_150.jpg	A1	home	\N
118	bathroom	ванная	en	https://cdn.pixabay.com/photo/2018/02/21/15/06/woman-3170568_150.jpg	A1	home	\N
127	desk	рабочий стол	en	https://cdn.pixabay.com/photo/2018/11/17/07/10/notebook-3820634_150.jpg	A1	home	\N
138	picture	картина	en	https://cdn.pixabay.com/photo/2017/08/30/17/26/please-2697951_150.jpg	A1	home	\N
150	clothes	одежда	en	https://cdn.pixabay.com/photo/2017/01/14/10/03/fashion-1979136_150.jpg	A1	home	\N
157	soap	мыло	en	https://cdn.pixabay.com/photo/2015/01/16/09/32/soap-601239_150.jpg	A1	home	\N
164	toilet	туалет	en	https://cdn.pixabay.com/photo/2013/05/14/16/56/wc-111092_150.jpg	A1	home	\N
171	new	новый	en	https://cdn.pixabay.com/photo/2016/10/31/14/55/nothing-1785760_150.jpg	A1	home	\N
180	wash	мыть	en	https://cdn.pixabay.com/photo/2023/09/28/15/59/clothes-pins-8281931_150.jpg	A1	home	\N
193	kettle	чайник	en	https://cdn.pixabay.com/photo/2016/11/25/15/13/teapots-1858601_150.jpg	A1	home	\N
200	dinner	ужин	en	https://cdn.pixabay.com/photo/2020/06/30/15/03/table-5356682_150.jpg	A1	food	\N
209	cheese	сыр	en	https://cdn.pixabay.com/photo/2018/08/29/19/01/fig-3640553_150.jpg	A1	food	\N
217	oil	масло	en	https://cdn.pixabay.com/photo/2017/07/16/22/22/bath-oil-2510783_150.jpg	A1	food	\N
225	burger	бургер	en	https://cdn.pixabay.com/photo/2022/08/29/17/44/burger-7419419_150.jpg	A1	food	\N
237	tomato	помидор	en	https://cdn.pixabay.com/photo/2014/09/15/16/53/tomatoes-447170_150.jpg	A1	food	\N
244	pea	горох	en	https://cdn.pixabay.com/photo/2018/06/14/20/19/sugar-pea-3475588_150.jpg	A1	food	\N
253	bottle	бутылка	en	https://cdn.pixabay.com/photo/2016/09/25/23/18/bottle-1694868_150.jpg	A1	drink	\N
381	street	улица	en	https://cdn.pixabay.com/photo/2013/03/02/02/41/alley-89197_150.jpg	A1	city	\N
385	ticket	билет	en	https://cdn.pixabay.com/photo/2017/11/24/10/43/ticket-2974645_150.jpg	A1	transport	\N
393	school	школа	en	https://cdn.pixabay.com/photo/2017/11/29/11/03/kids-2985782_150.jpg	A1	places	\N
269	good	хороший	en	https://cdn.pixabay.com/photo/2022/11/17/17/41/bear-7598582_150.jpg	A1	food	\N
276	animal	животное	en	https://cdn.pixabay.com/photo/2017/10/20/10/58/elephant-2870777_150.jpg	A1	animals	\N
285	goat	коза	en	https://cdn.pixabay.com/photo/2014/09/24/15/15/billy-goat-459232_150.jpg	A1	animals	\N
293	turtle	черепаха	en	https://cdn.pixabay.com/photo/2017/05/31/18/38/sea-2361247_150.jpg	A1	animals	\N
301	deer	олень	en	https://cdn.pixabay.com/photo/2016/08/11/17/53/roe-deer-1586373_150.jpg	A1	animals	\N
311	dolphin	дельфин	en	https://cdn.pixabay.com/photo/2013/11/01/11/13/dolphin-203875_150.jpg	A1	animals	\N
319	fly	муха	en	https://cdn.pixabay.com/photo/2024/08/21/18/25/flesh-fly-8987139_150.png	A1	animals	\N
329	head	голова	en	https://cdn.pixabay.com/photo/2016/09/28/08/28/art-1699977_150.jpg	A1	animals	\N
337	pet	домашний питомец	en	https://cdn.pixabay.com/photo/2020/03/31/19/20/dog-4988985_150.jpg	A1	animals	\N
348	fast	быстрый	en	https://cdn.pixabay.com/photo/2017/08/14/14/56/crisp-2640743_150.jpg	A1	animals	\N
358	father	папа	en	https://cdn.pixabay.com/photo/2016/11/14/04/45/bicycle-1822640_150.jpg	A1	animals	\N
368	train	поезд	en	https://cdn.pixabay.com/photo/2012/10/10/05/04/train-60539_150.jpg	A1	transport	\N
404	cinema	кинотеатр	en	https://cdn.pixabay.com/photo/2020/04/20/18/10/cinema-5069314_150.jpg	A1	places	\N
416	left	лево	en	https://cdn.pixabay.com/photo/2019/07/13/10/49/music-4334557_150.jpg	A1	city	\N
423	here	здесь	en	https://cdn.pixabay.com/photo/2018/11/03/15/51/here-3792307_150.png	A1	city	\N
433	wait	ждать	en	https://cdn.pixabay.com/photo/2020/03/17/20/16/ballet-4941738_150.jpg	A1	verbs	\N
867	answer	ответ	en	https://cdn.pixabay.com/photo/2015/08/08/20/52/busy-880800_150.jpg	A1	school	\N
874	language	язык	en	https://cdn.pixabay.com/photo/2017/03/20/04/37/gestures-2158259_150.jpg	A1	school	\N
895	salary	зарплата	en	https://cdn.pixabay.com/photo/2020/07/12/15/51/salary-5397714_150.jpg	A1	work	\N
907	read	читать	en	https://cdn.pixabay.com/photo/2016/11/18/16/49/books-1835753_150.jpg	A1	daily	\N
920	help	помогать	en	https://cdn.pixabay.com/photo/2020/05/24/23/44/hands-5216585_150.jpg	A1	daily	\N
1419	month	месяц	en	https://cdn.pixabay.com/photo/2022/06/12/18/31/lovers-7258609_150.jpg	A1	time	\N
1430	second	секунда	en	https://cdn.pixabay.com/photo/2016/01/27/04/32/books-1163695_150.jpg	A1	time	\N
1438	three	три	en	https://cdn.pixabay.com/photo/2016/09/03/01/03/bottles-1640819_150.jpg	A1	numbers	\N
1445	ten	десять	en	https://cdn.pixabay.com/photo/2016/04/25/23/53/euro-1353420_150.jpg	A1	numbers	\N
1452	thirty	тридцать	en	https://cdn.pixabay.com/photo/2020/03/09/06/18/camera-4914690_150.jpg	A1	numbers	\N
1459	green	зелёный	en	https://cdn.pixabay.com/photo/2018/05/04/21/22/meadow-3375052_150.jpg	A1	colors	\N
1468	dark	тёмный	en	https://cdn.pixabay.com/photo/2016/11/29/13/12/cloudy-1869753_150.jpg	A1	colors	\N
1477	jacket	куртка	en	https://cdn.pixabay.com/photo/2017/08/21/19/00/woman-2666433_150.jpg	A1	clothes	\N
2056	face	лицо	en	https://cdn.pixabay.com/photo/2016/10/04/08/07/face-painting-1713769_150.jpg	A1	body	\N
2070	heart	сердце	en	https://cdn.pixabay.com/photo/2018/02/12/10/45/heart-3147976_150.jpg	A1	body	\N
2079	medicine	лекарство	en	https://cdn.pixabay.com/photo/2016/11/22/23/32/medications-1851178_150.jpg	A1	health	\N
2828	be	быть	en	\N	A1	verbs	\N
3792	I	я	en	\N	A1	pronouns	\N
3799	my	мой	en	\N	A1	pronouns	\N
3820	to	к/в	en	\N	A1	prepositions	\N
3819	at	у/в	en	\N	A1	prepositions	\N
3833	hi	привет	en	\N	A1	phrases	\N
3839	no	нет	en	\N	A1	phrases	\N
3815	which	какой	en	\N	A1	questions	\N
2100	lake	озеро	en	https://cdn.pixabay.com/photo/2020/06/24/20/41/truebsee-5337646_150.jpg	A1	nature	\N
2108	earth	земля	en	https://cdn.pixabay.com/photo/2017/03/03/09/49/earth-2113656_150.jpg	A1	nature	\N
2119	cloud	облако	en	https://cdn.pixabay.com/photo/2022/08/08/13/59/cloud-of-bunch-of-7372799_150.jpg	A1	weather	\N
2128	spring	весна	en	https://cdn.pixabay.com/photo/2017/03/13/11/14/crocus-2139395_150.jpg	A1	weather	\N
2778	travel	путешествие	en	https://cdn.pixabay.com/photo/2017/06/05/11/01/airport-2373727_150.jpg	A1	travel	\N
2806	fly	лететь	en	https://cdn.pixabay.com/photo/2024/08/21/18/25/flesh-fly-8987139_150.png	A1	transport	\N
2819	card	карта	en	https://cdn.pixabay.com/photo/2014/02/01/17/50/money-256281_150.jpg	A1	shopping	\N
2835	see	видеть	en	https://cdn.pixabay.com/photo/2015/03/11/19/19/violet-669046_150.jpg	A1	verbs	\N
2842	love	любить	en	https://cdn.pixabay.com/photo/2017/10/11/11/31/roses-2840743_150.jpg	A1	verbs	\N
3624	long	длинный	en	https://cdn.pixabay.com/photo/2023/02/03/15/27/bird-7765384_150.jpg	A1	adjectives	\N
3678	traffic	движение	en	https://cdn.pixabay.com/photo/2022/05/22/11/10/highway-7213206_150.jpg	A1	city	\N
3687	north	север	en	https://cdn.pixabay.com/photo/2019/12/08/19/50/winter-4682051_150.jpg	A1	city	\N
3773	cut	резать	en	https://cdn.pixabay.com/photo/2014/12/20/14/03/vegetables-573961_150.jpg	A1	cooking	\N
3784	order	заказ	en	https://cdn.pixabay.com/photo/2016/08/23/12/37/files-1614223_150.jpg	A1	restaurant	\N
3803	our	наш	en	https://cdn.pixabay.com/photo/2014/10/20/22/22/budapest-495752_150.jpg	A1	pronouns	\N
2856	forget	забывать	en	https://cdn.pixabay.com/photo/2020/05/07/20/12/forget-me-not-5143015_150.jpg	A1	verbs	\N
3608	bored	скучающий	en	https://cdn.pixabay.com/photo/2015/04/20/13/12/little-boy-731165_150.jpg	A1	emotions	\N
3615	smile	улыбка	en	https://cdn.pixabay.com/photo/2017/08/02/23/58/people-2574170_150.jpg	A1	emotions	\N
3825	about	о/об	en	https://cdn.pixabay.com/photo/2014/06/18/18/42/running-shoe-371625_150.jpg	A1	prepositions	\N
3836	thanks	спасибо	en	https://cdn.pixabay.com/photo/2014/06/04/16/41/thank-you-362164_150.jpg	A1	phrases	\N
3846	how are you	как дела	en	https://cdn.pixabay.com/photo/2016/11/02/14/32/lotte-world-tower-1791802_150.jpg	A1	phrases	\N
3885	hand	рука	en	https://cdn.pixabay.com/photo/2020/02/21/12/58/toddler-hand-4867454_150.jpg	A1	body	\N
18	boy	мальчик	en	https://cdn.pixabay.com/photo/2016/08/13/13/45/boy-1590771_150.jpg	A1	people	\N
21	baby	малыш	en	https://cdn.pixabay.com/photo/2023/06/11/14/38/baby-8056153_150.jpg	A1	people	\N
24	son	сын	en	https://cdn.pixabay.com/photo/2016/11/14/04/45/bicycle-1822640_150.jpg	A1	people	\N
27	sister	сестра	en	https://cdn.pixabay.com/photo/2015/06/22/08/38/siblings-817369_150.jpg	A1	people	\N
29	friend	друг	en	https://cdn.pixabay.com/photo/2023/08/23/12/57/young-8208513_150.jpg	A1	people	\N
34	wife	жена	en	https://cdn.pixabay.com/photo/2019/05/24/18/41/marriage-4226896_150.jpg	A1	people	\N
36	teacher	учитель	en	https://cdn.pixabay.com/photo/2022/10/17/15/55/meditate-7528123_150.jpg	A1	people	\N
41	worker	рабочий	en	https://cdn.pixabay.com/photo/2021/06/09/01/55/worker-6322085_150.jpg	A1	people	\N
43	cook	повар	en	https://cdn.pixabay.com/photo/2017/03/10/13/57/cooking-2132874_150.jpg	A1	people	\N
47	neighbor	сосед	en	https://cdn.pixabay.com/photo/2018/05/23/22/37/chinchillas-3425370_150.jpg	A1	people	\N
51	student	студент	en	https://cdn.pixabay.com/photo/2017/02/27/23/34/college-2104580_150.jpg	A1	people	\N
54	leader	лидер	en	https://cdn.pixabay.com/photo/2018/04/08/08/18/smilies-3300636_150.jpg	A1	people	\N
57	boyfriend	парень	en	https://cdn.pixabay.com/photo/2021/01/06/21/50/couple-5895730_150.jpg	A1	people	\N
59	parent	родитель	en	https://cdn.pixabay.com/photo/2020/06/21/12/37/deer-5324645_150.jpg	A1	people	\N
62	uncle	дядя	en	https://cdn.pixabay.com/photo/2019/01/08/11/56/taibaishan-3921026_150.jpg	A1	people	\N
3920	hear	слышать	en	https://cdn.pixabay.com/photo/2016/03/23/13/36/frogs-1274769_150.jpg	A1	verbs	\N
3	house	дом	en	https://cdn.pixabay.com/photo/2014/07/10/17/18/large-home-389271_150.jpg	A1	\N	\N
66	adult	взрослый	en	https://cdn.pixabay.com/photo/2016/11/29/06/46/adult-1867889_150.jpg	A1	people	\N
72	rich	богатый	en	https://cdn.pixabay.com/photo/2013/07/18/10/56/gold-163519_150.jpg	A1	people	\N
75	sad	грустный	en	https://cdn.pixabay.com/photo/2020/11/06/15/33/woman-5718089_150.jpg	A1	people	\N
78	funny	смешной	en	https://cdn.pixabay.com/photo/2015/08/09/14/26/frog-881654_150.jpg	A1	people	\N
81	tall	высокий	en	https://cdn.pixabay.com/photo/2022/10/26/18/19/architecture-7549184_150.jpg	A1	people	\N
83	beautiful	красивый	en	https://cdn.pixabay.com/photo/2013/05/11/20/44/spring-flowers-110671_150.jpg	A1	people	\N
86	baby	младенец	en	https://cdn.pixabay.com/photo/2023/06/11/14/38/baby-8056153_150.jpg	A1	people	\N
94	member	член группы	en	https://cdn.pixabay.com/photo/2016/09/29/20/19/member-1703690_150.jpg	A1	people	\N
97	actor	актёр	en	https://cdn.pixabay.com/photo/2018/07/06/19/48/charles-chaplin-3521070_150.jpg	A1	people	\N
100	player	игрок	en	https://cdn.pixabay.com/photo/2015/01/26/22/40/child-613199_150.jpg	A1	people	\N
103	manager	менеджер	en	https://cdn.pixabay.com/photo/2020/04/19/18/46/company-5064997_150.jpg	A1	people	\N
64	cousin	двоюродный брат/сестра	en	https://cdn.pixabay.com/photo/2019/02/21/13/32/netflix-4011345_150.jpg	A1	people	\N
227	banana	банан	en	https://cdn.pixabay.com/photo/2015/11/05/23/08/banana-1025109_150.jpg	A1	food	\N
230	grape	виноград	en	https://cdn.pixabay.com/photo/2021/01/05/05/30/grapes-5889697_150.jpg	A1	food	\N
232	peach	персик	en	https://cdn.pixabay.com/photo/2017/08/11/17/41/peach-2632182_150.jpg	A1	food	\N
235	melon	дыня	en	https://cdn.pixabay.com/photo/2021/04/19/11/06/melon-6191136_150.jpg	A1	food	\N
238	onion	лук	en	https://cdn.pixabay.com/photo/2016/03/05/19/14/onions-1238332_150.jpg	A1	food	\N
240	cucumber	огурец	en	https://cdn.pixabay.com/photo/2019/07/03/11/41/cucumber-4314342_150.jpg	A1	food	\N
245	mushroom	гриб	en	https://cdn.pixabay.com/photo/2014/11/27/10/04/fly-agaric-547324_150.jpg	A1	food	\N
246	tea	чай	en	https://cdn.pixabay.com/photo/2015/07/02/20/37/cup-829527_150.jpg	A1	drink	\N
251	beer	пиво	en	https://cdn.pixabay.com/photo/2021/06/30/17/09/beer-6377244_150.jpg	A1	drink	\N
254	cup	чашка	en	https://cdn.pixabay.com/photo/2018/01/31/09/57/coffee-3120750_150.jpg	A1	drink	\N
258	fork	вилка	en	https://cdn.pixabay.com/photo/2016/06/10/16/32/potatoes-1448405_150.jpg	A1	food	\N
260	spoon	ложка	en	https://cdn.pixabay.com/photo/2014/11/24/14/35/pot-544071_150.jpg	A1	food	\N
265	salty	солёный	en	https://cdn.pixabay.com/photo/2024/08/08/17/13/salt-8955103_150.jpg	A1	food	\N
270	bad	плохой	en	https://cdn.pixabay.com/photo/2022/06/28/15/21/bach-7289941_150.jpg	A1	food	\N
272	thirsty	хочется пить	en	https://cdn.pixabay.com/photo/2016/01/30/17/41/elephants-1170111_150.jpg	A1	food	\N
275	sell	продавать	en	https://cdn.pixabay.com/photo/2016/11/23/14/56/bazaar-1853361_150.jpg	A1	food	\N
281	horse	лошадь	en	https://cdn.pixabay.com/photo/2014/12/08/17/52/horse-561221_150.jpg	A1	animals	\N
284	sheep	овца	en	https://cdn.pixabay.com/photo/2020/02/01/14/48/sheep-4810513_150.jpg	A1	animals	\N
288	rabbit	кролик	en	https://cdn.pixabay.com/photo/2014/06/21/08/43/rabbit-373691_150.jpg	A1	animals	\N
108	room	комната	en	https://cdn.pixabay.com/photo/2016/11/30/08/48/bedroom-1872196_150.jpg	A1	home	\N
112	floor	пол	en	https://cdn.pixabay.com/photo/2021/04/27/18/55/nature-6212211_150.jpg	A1	home	\N
115	garden	сад	en	https://cdn.pixabay.com/photo/2012/08/06/00/53/bridge-53769_150.jpg	A1	home	\N
117	bedroom	спальня	en	https://cdn.pixabay.com/photo/2016/11/19/13/06/bed-1839183_150.jpg	A1	home	\N
120	garage	гараж	en	https://cdn.pixabay.com/photo/2016/11/29/03/53/house-1867187_150.jpg	A1	home	\N
123	table	стол	en	https://cdn.pixabay.com/photo/2020/06/30/15/03/table-5356682_150.jpg	A1	home	\N
126	sofa	диван	en	https://cdn.pixabay.com/photo/2016/11/30/08/48/bedroom-1872196_150.jpg	A1	home	\N
129	box	коробка	en	https://cdn.pixabay.com/photo/2016/09/03/23/34/cashbox-1642989_150.jpg	A1	home	\N
132	mirror	зеркало	en	https://cdn.pixabay.com/photo/2018/12/08/22/42/mirror-3864155_150.jpg	A1	home	\N
135	key	ключ	en	https://cdn.pixabay.com/photo/2017/03/16/08/35/key-2148476_150.jpg	A1	home	\N
139	photo	фото	en	https://cdn.pixabay.com/photo/2023/12/06/21/07/photo-8434386_150.jpg	A1	home	\N
141	paper	бумага	en	https://cdn.pixabay.com/photo/2016/05/14/22/22/paper-1392749_150.jpg	A1	home	\N
144	computer	компьютер	en	https://cdn.pixabay.com/photo/2016/11/23/14/45/coding-1853305_150.jpg	A1	home	\N
147	radio	радио	en	https://cdn.pixabay.com/photo/2016/09/20/13/46/radio-1682531_150.jpg	A1	home	\N
149	bag	сумка	en	https://cdn.pixabay.com/photo/2016/11/23/18/12/bag-1854148_150.jpg	A1	home	\N
154	coat	пальто	en	https://cdn.pixabay.com/photo/2023/10/03/09/59/bridge-8291058_150.jpg	A1	home	\N
156	towel	полотенце	en	https://cdn.pixabay.com/photo/2014/12/19/17/22/chicks-573377_150.jpg	A1	home	\N
160	toothpaste	зубная паста	en	https://cdn.pixabay.com/photo/2018/03/01/16/43/toothbrush-3191097_150.jpg	A1	home	\N
162	bath	ванна	en	https://cdn.pixabay.com/photo/2017/07/12/22/52/woman-2498668_150.jpg	A1	home	\N
166	dirty	грязный	en	https://cdn.pixabay.com/photo/2016/01/13/22/48/pottery-1139047_150.jpg	A1	home	\N
169	big	большой	en	https://cdn.pixabay.com/photo/2020/08/19/00/13/sea-5499649_150.jpg	A1	home	\N
173	hot	горячий	en	https://cdn.pixabay.com/photo/2020/09/21/05/57/coffee-5589036_150.jpg	A1	home	\N
175	floor	этаж/пол	en	https://cdn.pixabay.com/photo/2021/04/27/18/55/nature-6212211_150.jpg	A1	home	\N
179	cook	готовить	en	https://cdn.pixabay.com/photo/2017/03/10/13/57/cooking-2132874_150.jpg	A1	home	\N
182	sleep	спать	en	https://cdn.pixabay.com/photo/2017/04/03/10/42/woman-2197947_150.jpg	A1	home	\N
185	live	жить	en	https://cdn.pixabay.com/photo/2016/11/19/09/57/violins-1838390_150.jpg	A1	home	\N
189	repair	чинить	en	https://cdn.pixabay.com/photo/2015/07/11/14/53/plumbing-840835_150.jpg	A1	home	\N
194	plate	тарелка	en	https://cdn.pixabay.com/photo/2017/05/07/08/56/pancakes-2291908_150.jpg	A1	home	\N
196	food	еда	en	https://cdn.pixabay.com/photo/2017/12/10/14/47/pizza-3010062_150.jpg	A1	food	\N
199	lunch	обед	en	https://cdn.pixabay.com/photo/2018/07/14/21/30/club-sandwich-3538455_150.jpg	A1	food	\N
203	pasta	макароны	en	https://cdn.pixabay.com/photo/2014/12/08/09/45/pasta-560657_150.jpg	A1	food	\N
206	chicken	курица	en	https://cdn.pixabay.com/photo/2014/05/20/21/25/bird-349035_150.jpg	A1	food	\N
210	butter	масло	en	https://cdn.pixabay.com/photo/2015/03/21/18/04/peanut-butter-684021_150.jpg	A1	food	\N
213	cream	сливки	en	https://cdn.pixabay.com/photo/2017/04/18/15/10/strawberry-ice-cream-2239377_150.jpg	A1	food	\N
218	cake	торт	en	https://cdn.pixabay.com/photo/2016/02/29/00/19/cake-1227842_150.jpg	A1	food	\N
220	chocolate	шоколад	en	https://cdn.pixabay.com/photo/2010/12/13/10/13/chocolate-2554_150.jpg	A1	food	\N
223	sandwich	бутерброд	en	https://cdn.pixabay.com/photo/2023/05/29/17/01/hamburger-8026582_150.jpg	A1	food	\N
295	tiger	тигр	en	https://cdn.pixabay.com/photo/2017/01/12/21/42/tiger-1975790_150.jpg	A1	animals	\N
298	bear	медведь	en	https://cdn.pixabay.com/photo/2023/09/25/19/52/bear-8275920_150.jpg	A1	animals	\N
300	fox	лиса	en	https://cdn.pixabay.com/photo/2019/08/06/10/40/leuchtpunkt-fox-4388014_150.jpg	A1	animals	\N
303	zebra	зебра	en	https://cdn.pixabay.com/photo/2022/02/06/13/31/animal-6997104_150.jpg	A1	animals	\N
308	cheetah	гепард	en	https://cdn.pixabay.com/photo/2023/09/09/09/03/cheetah-8242729_150.png	A1	animals	\N
310	whale	кит	en	https://cdn.pixabay.com/photo/2017/02/09/12/07/ocean-2051760_150.jpg	A1	animals	\N
313	crab	краб	en	https://cdn.pixabay.com/photo/2023/03/21/10/30/crab-7866915_150.jpg	A1	animals	\N
317	bee	пчела	en	https://cdn.pixabay.com/photo/2020/05/25/18/35/bee-5219887_150.jpg	A1	animals	\N
320	spider	паук	en	https://cdn.pixabay.com/photo/2014/09/06/14/23/spider-436947_150.jpg	A1	animals	\N
326	tail	хвост	en	https://cdn.pixabay.com/photo/2021/02/06/19/15/tail-light-5989090_150.jpg	A1	animals	\N
328	wing	крыло	en	https://cdn.pixabay.com/photo/2025/01/02/23/26/butterfly-9306937_150.jpg	A1	animals	\N
332	nose	нос	en	https://cdn.pixabay.com/photo/2021/11/21/17/47/animal-6814822_150.jpg	A1	animals	\N
336	wild	дикий	en	https://cdn.pixabay.com/photo/2017/07/24/19/57/tiger-2535888_150.jpg	A1	animals	\N
339	zoo	зоопарк	en	https://cdn.pixabay.com/photo/2023/07/17/13/50/baby-snow-leopard-8132690_150.jpg	A1	animals	\N
342	run	бегать	en	https://cdn.pixabay.com/photo/2015/02/13/04/27/run-634702_150.jpg	A1	animals	\N
349	slow	медленный	en	https://cdn.pixabay.com/photo/2022/10/16/05/02/snail-7524205_150.jpg	A1	animals	\N
352	friendly	дружелюбный	en	https://cdn.pixabay.com/photo/2026/07/03/19/38/19-38-36-577_150.jpg	A1	animals	\N
357	mother	мама	en	https://cdn.pixabay.com/photo/2022/04/05/19/34/motherhood-7114294_150.jpg	A1	animals	\N
362	sea	море	en	https://cdn.pixabay.com/photo/2021/12/29/14/47/water-6901805_150.jpg	A1	animals	\N
364	grass	трава	en	https://cdn.pixabay.com/photo/2014/02/27/16/09/grass-275986_150.jpg	A1	animals	\N
370	bike	велосипед	en	https://cdn.pixabay.com/photo/2015/08/27/09/06/bike-909690_150.jpg	A1	transport	\N
373	taxi	такси	en	https://cdn.pixabay.com/photo/2014/01/04/13/34/taxi-238478_150.jpg	A1	transport	\N
376	ship	корабль	en	https://cdn.pixabay.com/photo/2024/05/28/12/28/ship-8793759_150.jpg	A1	transport	\N
379	airport	аэропорт	en	https://cdn.pixabay.com/photo/2019/09/05/15/25/airbus-4454338_150.jpg	A1	transport	\N
382	bridge	мост	en	https://cdn.pixabay.com/photo/2017/09/20/06/27/bridge-2767545_150.jpg	A1	city	\N
384	map	карта	en	https://cdn.pixabay.com/photo/2017/07/22/11/46/adventure-2528477_150.jpg	A1	city	\N
387	town	городок	en	https://cdn.pixabay.com/photo/2020/08/30/09/22/people-5528959_150.jpg	A1	city	\N
391	building	здание	en	https://cdn.pixabay.com/photo/2018/02/27/06/30/skyscrapers-3184798_150.jpg	A1	city	\N
395	bank	банк	en	https://cdn.pixabay.com/photo/2017/11/01/11/34/bank-2907728_150.jpg	A1	places	\N
398	restaurant	ресторан	en	https://cdn.pixabay.com/photo/2016/02/10/13/35/hotel-1191718_150.jpg	A1	places	\N
400	hotel	отель	en	https://cdn.pixabay.com/photo/2016/10/18/09/02/hotel-1749602_150.jpg	A1	places	\N
402	library	библиотека	en	https://cdn.pixabay.com/photo/2017/08/06/22/01/books-2596809_150.jpg	A1	places	\N
405	office	офис	en	https://cdn.pixabay.com/photo/2015/04/20/06/46/office-730681_150.jpg	A1	places	\N
407	factory	фабрика	en	https://cdn.pixabay.com/photo/2021/05/03/13/24/sunset-6226244_150.jpg	A1	work	\N
413	post office	почта	en	https://cdn.pixabay.com/photo/2015/09/04/23/28/wordpress-923188_150.jpg	A1	places	\N
415	bus stop	автобусная остановка	en	https://cdn.pixabay.com/photo/2020/07/26/18/11/stop-5440282_150.jpg	A1	transport	\N
417	right	право	en	https://cdn.pixabay.com/photo/2013/12/29/10/15/directory-235079_150.jpg	A1	city	\N
420	far	далеко	en	https://cdn.pixabay.com/photo/2020/03/26/09/01/fog-4969649_150.jpg	A1	city	\N
424	there	там	en	https://cdn.pixabay.com/photo/2018/11/03/15/51/here-3792307_150.png	A1	city	\N
427	come	приходить	en	https://cdn.pixabay.com/photo/2015/03/29/08/55/entrepreneur-696976_150.png	A1	verbs	\N
429	fly	летать	en	https://cdn.pixabay.com/photo/2024/08/21/18/25/flesh-fly-8987139_150.png	A1	verbs	\N
432	turn	поворачивать	en	https://cdn.pixabay.com/photo/2020/05/18/21/21/manege-5188459_150.jpg	A1	verbs	\N
435	leave	уезжать	en	https://cdn.pixabay.com/photo/2022/11/20/18/32/winter-7604917_150.jpg	A1	verbs	\N
866	question	вопрос	en	https://cdn.pixabay.com/photo/2014/09/27/13/46/question-mark-463497_150.jpg	A1	school	\N
869	exam	экзамен	en	https://cdn.pixabay.com/photo/2015/04/20/18/58/student-732012_150.jpg	A1	school	\N
872	math	математика	en	https://cdn.pixabay.com/photo/2016/11/29/01/16/abacus-1866497_150.jpg	A1	school	\N
875	word	слово	en	https://cdn.pixabay.com/photo/2016/01/30/22/04/typewriter-1170657_150.jpg	A1	school	\N
877	job	работа/должность	en	https://cdn.pixabay.com/photo/2020/07/08/04/12/work-5382501_150.jpg	A1	work	\N
894	pay	платить	en	https://cdn.pixabay.com/photo/2018/02/24/20/39/clock-3179167_150.jpg	A1	work	\N
897	get up	вставать	en	https://cdn.pixabay.com/photo/2020/02/05/20/35/lift-4822344_150.jpg	A1	daily	\N
902	drink	пить	en	https://cdn.pixabay.com/photo/2016/03/30/19/28/coffee-break-1291381_150.jpg	A1	daily	\N
909	listen	слушать	en	https://cdn.pixabay.com/photo/2017/01/18/17/14/girl-1990347_150.jpg	A1	daily	\N
917	close	закрывать	en	https://cdn.pixabay.com/photo/2015/12/13/02/07/pebble-1090536_150.jpg	A1	daily	\N
921	call	звонить	en	https://cdn.pixabay.com/photo/2017/05/01/14/59/call-center-2275745_150.jpg	A1	daily	\N
2830	do	делать	en	\N	A1	verbs	\N
1420	year	год	en	https://cdn.pixabay.com/photo/2021/12/27/16/40/sylvester-6897648_150.jpg	A1	time	\N
1422	tomorrow	завтра	en	https://cdn.pixabay.com/photo/2012/12/29/21/11/sunrise-73074_150.jpg	A1	time	\N
1425	afternoon	день	en	https://cdn.pixabay.com/photo/2018/11/06/14/01/happy-valentines-day-3798371_150.jpg	A1	time	\N
1428	hour	час	en	https://cdn.pixabay.com/photo/2023/06/22/04/19/rye-8080482_150.jpg	A1	time	\N
1432	late	поздно	en	https://cdn.pixabay.com/photo/2016/09/29/16/56/hourglass-1703330_150.jpg	A1	time	\N
1435	after	после	en	https://cdn.pixabay.com/photo/2017/02/20/05/00/bloom-2081623_150.jpg	A1	time	\N
1437	two	два	en	https://cdn.pixabay.com/photo/2014/06/25/21/46/bikini-377487_150.jpg	A1	numbers	\N
1442	seven	семь	en	https://cdn.pixabay.com/photo/2016/06/17/00/27/seven-sisters-1462388_150.jpg	A1	numbers	\N
1444	nine	девять	en	https://cdn.pixabay.com/photo/2012/02/27/16/58/armadillo-17446_150.jpg	A1	numbers	\N
1447	twelve	двенадцать	en	https://cdn.pixabay.com/photo/2018/03/11/14/09/eggs-3216877_150.jpg	A1	numbers	\N
1450	fifteen	пятнадцать	en	https://cdn.pixabay.com/photo/2015/12/26/13/45/moon-1108686_150.jpg	A1	numbers	\N
1453	hundred	сто	en	https://cdn.pixabay.com/photo/2023/03/13/16/10/banknotes-7850299_150.jpg	A1	numbers	\N
1456	color	цвет	en	https://cdn.pixabay.com/photo/2022/11/15/08/40/dry-plant-7593485_150.jpg	A1	colors	\N
1460	yellow	жёлтый	en	https://cdn.pixabay.com/photo/2022/02/07/14/58/hibiscus-6999568_150.jpg	A1	colors	\N
1462	white	белый	en	https://cdn.pixabay.com/photo/2021/07/14/18/34/poppy-6466826_150.jpg	A1	colors	\N
1465	brown	коричневый	en	https://cdn.pixabay.com/photo/2020/04/27/18/33/horse-5101069_150.jpg	A1	colors	\N
1467	purple	фиолетовый	en	https://cdn.pixabay.com/photo/2015/03/11/19/19/violet-669046_150.jpg	A1	colors	\N
1472	t-shirt	футболка	en	https://cdn.pixabay.com/photo/2016/06/20/04/30/asian-man-1468032_150.jpg	A1	clothes	\N
1476	skirt	юбка	en	https://cdn.pixabay.com/photo/2022/12/04/15/42/woman-7634819_150.jpg	A1	clothes	\N
1482	cap	кепка	en	https://cdn.pixabay.com/photo/2016/05/31/11/26/baby-1426651_150.jpg	A1	clothes	\N
1485	belt	ремень	en	https://cdn.pixabay.com/photo/2017/03/20/20/36/blue-jeans-2160265_150.jpg	A1	clothes	\N
1488	put on	надеть	en	https://cdn.pixabay.com/photo/2016/03/31/04/50/blush-1292054_150.jpg	A1	clothes	\N
2057	hair	волосы	en	https://cdn.pixabay.com/photo/2017/06/15/11/40/beautiful-2405131_150.jpg	A1	body	\N
2064	arm	рука	en	https://cdn.pixabay.com/photo/2017/08/22/00/38/meadow-2667461_150.jpg	A1	body	\N
2068	foot	ступня	en	https://cdn.pixabay.com/photo/2021/09/22/23/52/father-6648076_150.jpg	A1	body	\N
2071	skin	кожа	en	https://cdn.pixabay.com/photo/2019/03/24/13/43/elephant-4077701_150.jpg	A1	body	\N
2075	sick	больной	en	https://cdn.pixabay.com/photo/2021/03/26/15/21/beautiful-6126170_150.jpg	A1	health	\N
2080	pain	боль	en	https://cdn.pixabay.com/photo/2016/11/21/15/45/man-1846050_150.jpg	A1	health	\N
2082	cold	простуда	en	https://cdn.pixabay.com/photo/2024/12/31/23/46/bridge-9302956_150.jpg	A1	health	\N
2085	rest	отдых	en	https://cdn.pixabay.com/photo/2022/04/19/08/32/relax-7142183_150.jpg	A1	health	\N
2091	hurt	болеть	en	https://cdn.pixabay.com/photo/2016/11/21/15/45/man-1846050_150.jpg	A1	health	\N
2096	flower	цветок	en	https://cdn.pixabay.com/photo/2023/04/19/09/34/flower-7937334_150.jpg	A1	nature	\N
2102	ocean	океан	en	https://cdn.pixabay.com/photo/2020/08/19/00/13/sea-5499649_150.jpg	A1	nature	\N
2104	hill	холм	en	https://cdn.pixabay.com/photo/2020/07/19/09/57/hill-5419527_150.jpg	A1	nature	\N
2107	sand	песок	en	https://cdn.pixabay.com/photo/2024/03/16/15/42/sand-8637315_150.jpg	A1	nature	\N
2110	sun	солнце	en	https://cdn.pixabay.com/photo/2018/03/30/13/01/sun-3275314_150.jpg	A1	nature	\N
2114	weather	погода	en	https://cdn.pixabay.com/photo/2018/08/23/07/35/new-year-background-3625405_150.jpg	A1	weather	\N
2117	snow	снег	en	https://cdn.pixabay.com/photo/2022/12/10/11/05/snow-7646952_150.jpg	A1	weather	\N
2120	storm	буря	en	https://cdn.pixabay.com/photo/2015/11/22/15/16/lightning-1056419_150.jpg	A1	weather	\N
2123	warm	тёплый	en	https://cdn.pixabay.com/photo/2022/06/29/08/26/pour-7291236_150.jpg	A1	weather	\N
2127	season	время года	en	https://cdn.pixabay.com/photo/2018/09/23/18/56/pumpkin-3698130_150.jpg	A1	weather	\N
2130	autumn	осень	en	https://cdn.pixabay.com/photo/2016/11/01/18/19/trees-1789120_150.jpg	A1	weather	\N
2133	degree	градус	en	https://cdn.pixabay.com/photo/2017/04/03/07/29/dortmund-2197673_150.jpg	A1	weather	\N
2780	holiday	отпуск	en	https://cdn.pixabay.com/photo/2022/10/05/05/40/sunset-7499759_150.jpg	A1	travel	\N
2787	passport	паспорт	en	https://cdn.pixabay.com/photo/2019/04/04/03/11/sella-capital-4101892_150.jpg	A1	travel	\N
2807	stop	остановка	en	https://cdn.pixabay.com/photo/2019/01/30/11/52/businessman-3964425_150.jpg	A1	transport	\N
2816	expensive	дорогой	en	https://cdn.pixabay.com/photo/2016/05/05/18/01/coupe-1374436_150.jpg	A1	shopping	\N
2818	cash	наличные	en	https://cdn.pixabay.com/photo/2016/09/03/23/34/cashbox-1642989_150.jpg	A1	shopping	\N
2829	have	иметь	en	https://cdn.pixabay.com/photo/2018/01/27/17/38/fruit-3111745_150.jpg	A1	verbs	\N
2833	give	давать	en	https://cdn.pixabay.com/photo/2020/04/24/16/01/drink-5087479_150.jpg	A1	verbs	\N
2836	look	смотреть	en	https://cdn.pixabay.com/photo/2024/02/21/13/15/lipstick-8587707_150.jpg	A1	verbs	\N
2838	think	думать	en	https://cdn.pixabay.com/photo/2016/12/11/09/22/robot-1899013_150.jpg	A1	verbs	\N
2841	like	нравиться	en	https://cdn.pixabay.com/photo/2023/04/21/16/23/mongoose-7942222_150.jpg	A1	verbs	\N
2844	find	находить	en	https://cdn.pixabay.com/photo/2020/02/26/18/03/discover-4882439_150.jpg	A1	verbs	\N
3794	he	он	en	\N	A1	pronouns	\N
3796	it	это/оно	en	\N	A1	pronouns	\N
3797	we	мы	en	\N	A1	pronouns	\N
3817	in	в	en	\N	A1	prepositions	\N
3818	on	на	en	\N	A1	prepositions	\N
2847	ask	спрашивать	en	https://cdn.pixabay.com/photo/2017/05/24/22/57/ask-2341784_150.jpg	A1	verbs	\N
2848	tell	рассказывать	en	https://cdn.pixabay.com/photo/2020/05/31/22/11/stir-5244456_150.jpg	A1	verbs	\N
2849	say	сказать	en	https://cdn.pixabay.com/photo/2014/01/04/13/38/tin-can-238488_150.jpg	A1	verbs	\N
2853	learn	учить	en	https://cdn.pixabay.com/photo/2024/11/13/18/33/child-9195259_150.jpg	A1	verbs	\N
2854	teach	обучать	en	https://cdn.pixabay.com/photo/2017/01/10/01/32/teach-1968076_150.jpg	A1	verbs	\N
2855	remember	помнить	en	https://cdn.pixabay.com/photo/2017/11/04/11/16/jews-2917190_150.jpg	A1	verbs	\N
2857	understand	понимать	en	https://cdn.pixabay.com/photo/2017/09/10/19/08/boy-2736656_150.jpg	A1	verbs	\N
3604	angry	злой	en	https://cdn.pixabay.com/photo/2022/04/03/07/49/angry-7108276_150.jpg	A1	emotions	\N
3605	afraid	испуганный	en	https://cdn.pixabay.com/photo/2026/01/17/08/41/pet-10072662_150.jpg	A1	emotions	\N
3607	excited	взволнованный	en	https://cdn.pixabay.com/photo/2015/01/08/18/24/children-593313_150.jpg	A1	emotions	\N
3609	busy	занятый	en	https://cdn.pixabay.com/photo/2019/03/17/12/57/phone-4060860_150.jpg	A1	emotions	\N
3610	calm	спокойный	en	https://cdn.pixabay.com/photo/2013/04/04/12/34/mountains-100367_150.jpg	A1	emotions	\N
3611	worried	обеспокоенный	en	https://cdn.pixabay.com/photo/2021/03/01/14/40/girl-6059889_150.jpg	A1	emotions	\N
3613	hope	надежда	en	https://cdn.pixabay.com/photo/2019/11/29/17/05/hand-4661763_150.jpg	A1	emotions	\N
3614	fear	страх	en	https://cdn.pixabay.com/photo/2019/10/09/13/10/halloween-4537430_150.jpg	A1	emotions	\N
3616	laugh	смех	en	https://cdn.pixabay.com/photo/2016/01/24/14/27/frogs-1158958_150.jpg	A1	emotions	\N
3617	cry	плакать	en	https://cdn.pixabay.com/photo/2017/02/08/13/43/woman-2048905_150.jpg	A1	emotions	\N
3618	feel	чувствовать	en	https://cdn.pixabay.com/photo/2016/02/15/10/28/skin-1200933_150.jpg	A1	emotions	\N
3625	short	короткий	en	https://cdn.pixabay.com/photo/2026/02/14/17/57/veronika_andrews-short-eared-owl-10123513_150.jpg	A1	adjectives	\N
3626	high	высокий	en	https://cdn.pixabay.com/photo/2021/10/11/18/56/shoes-6701631_150.jpg	A1	adjectives	\N
3631	ugly	некрасивый	en	https://cdn.pixabay.com/photo/2014/09/02/15/28/styggkarret-433688_150.jpg	A1	adjectives	\N
3632	easy	лёгкий	en	https://cdn.pixabay.com/photo/2017/06/18/22/20/soap-bubbles-2417436_150.jpg	A1	adjectives	\N
3633	difficult	сложный	en	https://cdn.pixabay.com/photo/2017/01/13/09/23/magic-cube-1976725_150.jpg	A1	adjectives	\N
3652	place	место	en	https://cdn.pixabay.com/photo/2020/04/21/19/30/rome-5074421_150.jpg	A1	places	\N
3674	flat	квартира	en	https://cdn.pixabay.com/photo/2013/11/27/09/49/iceland-219182_150.jpg	A1	city	\N
3684	crossing	переход	en	https://cdn.pixabay.com/photo/2020/02/18/16/44/junction-4860035_150.jpg	A1	city	\N
3685	corner	угол	en	https://cdn.pixabay.com/photo/2016/09/18/20/47/football-1678992_150.jpg	A1	city	\N
3686	center	центр	en	https://cdn.pixabay.com/photo/2019/10/23/18/32/freudenberg-4572410_150.jpg	A1	city	\N
3688	south	юг	en	https://cdn.pixabay.com/photo/2020/03/16/11/10/austria-4936672_150.jpg	A1	city	\N
3689	east	восток	en	https://cdn.pixabay.com/photo/2023/10/10/15/12/landscape-8306693_150.jpg	A1	city	\N
3692	thing	вещь	en	https://cdn.pixabay.com/photo/2017/01/13/12/56/luggage-compartment-1977186_150.jpg	A1	objects	\N
3721	photo	фотография	en	https://cdn.pixabay.com/photo/2023/12/06/21/07/photo-8434386_150.jpg	A1	objects	\N
3733	beef	говядина	en	https://cdn.pixabay.com/photo/2018/07/01/15/08/beef-3509716_150.jpg	A1	food	\N
3770	pot	кастрюля	en	https://cdn.pixabay.com/photo/2017/05/27/03/20/succulents-2347550_150.jpg	A1	cooking	\N
3771	oven	духовка	en	https://cdn.pixabay.com/photo/2022/01/05/21/07/pizza-6918041_150.jpg	A1	cooking	\N
3774	mix	смешивать	en	https://cdn.pixabay.com/photo/2016/03/27/22/21/mixer-1284507_150.jpg	A1	cooking	\N
3775	boil	варить	en	https://cdn.pixabay.com/photo/2014/12/15/13/40/spaghetti-569067_150.jpg	A1	cooking	\N
3777	taste	пробовать вкус	en	https://cdn.pixabay.com/photo/2017/03/10/13/57/cooking-2132874_150.jpg	A1	cooking	\N
3781	thirsty	хотеть пить	en	https://cdn.pixabay.com/photo/2016/01/30/17/41/elephants-1170111_150.jpg	A1	cooking	\N
3783	menu	меню	en	https://cdn.pixabay.com/photo/2016/11/29/12/54/cafe-1869656_150.jpg	A1	restaurant	\N
3788	bill	счёт	en	https://cdn.pixabay.com/photo/2024/11/07/18/01/spoonbill-9181508_150.jpg	A1	restaurant	\N
3791	tip	чаевые	en	https://cdn.pixabay.com/photo/2022/04/08/11/48/fern-7119343_150.jpg	A1	restaurant	\N
3793	you	ты/вы	en	https://cdn.pixabay.com/photo/2021/11/10/18/21/woman-6784555_150.jpg	A1	pronouns	\N
3798	they	они	en	https://cdn.pixabay.com/photo/2013/09/16/19/47/children-183007_150.jpg	A1	pronouns	\N
3800	your	твой/ваш	en	https://cdn.pixabay.com/photo/2015/06/28/07/18/i-beg-your-pardon-824194_150.jpg	A1	pronouns	\N
3801	his	его	en	https://cdn.pixabay.com/photo/2020/05/09/07/41/cassettes-5148602_150.jpg	A1	pronouns	\N
3804	their	их	en	https://cdn.pixabay.com/photo/2017/03/29/15/59/small-cat-2185670_150.jpg	A1	pronouns	\N
3809	what	что	en	https://cdn.pixabay.com/photo/2017/09/03/18/56/what-2711657_150.jpg	A1	questions	\N
3813	why	почему	en	https://cdn.pixabay.com/photo/2018/08/29/01/34/life-3638969_150.jpg	A1	questions	\N
3821	from	из/от	en	https://cdn.pixabay.com/photo/2015/01/09/15/34/chunks-594496_150.jpg	A1	prepositions	\N
3826	under	под	en	https://cdn.pixabay.com/photo/2015/03/17/16/07/helm-677990_150.jpg	A1	prepositions	\N
3830	behind	позади	en	https://cdn.pixabay.com/photo/2015/05/09/13/45/woman-759688_150.jpg	A1	prepositions	\N
3832	hello	привет	en	https://cdn.pixabay.com/photo/2017/01/28/14/19/hello-2015466_150.jpg	A1	phrases	\N
3953	арбалет	crossbow	en	\N	1	history	\N
\.


--
-- Name: history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: translaytor
--

SELECT pg_catalog.setval('public.history_id_seq', 271, true);


--
-- Name: user_words_id_seq; Type: SEQUENCE SET; Schema: public; Owner: translaytor
--

SELECT pg_catalog.setval('public.user_words_id_seq', 14, true);


--
-- Name: word_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: translaytor
--

SELECT pg_catalog.setval('public.word_progress_id_seq', 624, true);


--
-- Name: words_id_seq; Type: SEQUENCE SET; Schema: public; Owner: translaytor
--

SELECT pg_catalog.setval('public.words_id_seq', 3953, true);


--
-- Name: daily_goal daily_goal_pkey; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.daily_goal
    ADD CONSTRAINT daily_goal_pkey PRIMARY KEY (telegram_id);


--
-- Name: history history_pkey; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.history
    ADD CONSTRAINT history_pkey PRIMARY KEY (id);


--
-- Name: learning_session learning_session_pkey; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.learning_session
    ADD CONSTRAINT learning_session_pkey PRIMARY KEY (telegram_id);


--
-- Name: study_session study_session_pkey; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.study_session
    ADD CONSTRAINT study_session_pkey PRIMARY KEY (telegram_id);


--
-- Name: user_words user_words_pkey; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.user_words
    ADD CONSTRAINT user_words_pkey PRIMARY KEY (id);


--
-- Name: user_words user_words_telegram_id_word_id_key; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.user_words
    ADD CONSTRAINT user_words_telegram_id_word_id_key UNIQUE (telegram_id, word_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (telegram_id);


--
-- Name: word_progress word_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.word_progress
    ADD CONSTRAINT word_progress_pkey PRIMARY KEY (id);


--
-- Name: word_progress word_progress_telegram_id_word_id_key; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.word_progress
    ADD CONSTRAINT word_progress_telegram_id_word_id_key UNIQUE (telegram_id, word_id);


--
-- Name: words words_pkey; Type: CONSTRAINT; Schema: public; Owner: translaytor
--

ALTER TABLE ONLY public.words
    ADD CONSTRAINT words_pkey PRIMARY KEY (id);


--
-- Name: idx_words_unique; Type: INDEX; Schema: public; Owner: translaytor
--

CREATE UNIQUE INDEX idx_words_unique ON public.words USING btree (word, translation, language);


--
-- PostgreSQL database dump complete
--

\unrestrict VCb2wQwf0JAgrUYon3fGvyYcCfrVSS1LGTvZGxKYBOmS0uGLDFQsQgiCWvf4gsq

