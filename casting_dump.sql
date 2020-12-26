--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

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
-- Name: actor; Type: TABLE; Schema: public; Owner: tonym
--

CREATE TABLE public.actor (
    id integer NOT NULL,
    name character varying,
    dob date,
    gender character varying
);


ALTER TABLE public.actor OWNER TO tonym;

--
-- Name: actor_id_seq; Type: SEQUENCE; Schema: public; Owner: tonym
--

CREATE SEQUENCE public.actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actor_id_seq OWNER TO tonym;

--
-- Name: actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tonym
--

ALTER SEQUENCE public.actor_id_seq OWNED BY public.actor.id;


--
-- Name: movie; Type: TABLE; Schema: public; Owner: tonym
--

CREATE TABLE public.movie (
    id integer NOT NULL,
    title character varying,
    release_date date
);


ALTER TABLE public.movie OWNER TO tonym;

--
-- Name: movie_id_seq; Type: SEQUENCE; Schema: public; Owner: tonym
--

CREATE SEQUENCE public.movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movie_id_seq OWNER TO tonym;

--
-- Name: movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tonym
--

ALTER SEQUENCE public.movie_id_seq OWNED BY public.movie.id;


--
-- Name: moviecast; Type: TABLE; Schema: public; Owner: tonym
--

CREATE TABLE public.moviecast (
    movie_id integer,
    actor_id integer
);


ALTER TABLE public.moviecast OWNER TO tonym;

--
-- Name: actor id; Type: DEFAULT; Schema: public; Owner: tonym
--

ALTER TABLE ONLY public.actor ALTER COLUMN id SET DEFAULT nextval('public.actor_id_seq'::regclass);


--
-- Name: movie id; Type: DEFAULT; Schema: public; Owner: tonym
--

ALTER TABLE ONLY public.movie ALTER COLUMN id SET DEFAULT nextval('public.movie_id_seq'::regclass);


--
-- Data for Name: actor; Type: TABLE DATA; Schema: public; Owner: tonym
--

COPY public.actor (id, name, dob, gender) FROM stdin;
1	Tony Mills	1970-12-13	M
2	Mary Poppins	1975-02-10	F
3	George Francios	1968-05-30	M
\.


--
-- Data for Name: movie; Type: TABLE DATA; Schema: public; Owner: tonym
--

COPY public.movie (id, title, release_date) FROM stdin;
1	Freebird	2018-10-04
2	April Fools	2020-04-01
\.


--
-- Data for Name: moviecast; Type: TABLE DATA; Schema: public; Owner: tonym
--

COPY public.moviecast (movie_id, actor_id) FROM stdin;
1	1
1	3
2	1
2	2
2	3
\.


--
-- Name: actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tonym
--

SELECT pg_catalog.setval('public.actor_id_seq', 3, true);


--
-- Name: movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tonym
--

SELECT pg_catalog.setval('public.movie_id_seq', 2, true);


--
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: tonym
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (id);


--
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: tonym
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);


--
-- Name: moviecast moviecast_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tonym
--

ALTER TABLE ONLY public.moviecast
    ADD CONSTRAINT moviecast_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actor(id);


--
-- Name: moviecast moviecast_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tonym
--

ALTER TABLE ONLY public.moviecast
    ADD CONSTRAINT moviecast_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movie(id);


--
-- PostgreSQL database dump complete
--

