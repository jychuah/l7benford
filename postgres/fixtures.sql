--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1 (Debian 13.1-1.pgdg100+1)
-- Dumped by pg_dump version 13.1 (Debian 13.1-1.pgdg100+1)

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
-- Name: benford; Type: TABLE; Schema: public; Owner: benford
--

CREATE TABLE public.benford (
    id integer NOT NULL,
    filename character varying(64),
    contents bytea,
    metadata json
);


ALTER TABLE public.benford OWNER TO benford;

--
-- Name: benford_id_seq; Type: SEQUENCE; Schema: public; Owner: benford
--

CREATE SEQUENCE public.benford_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.benford_id_seq OWNER TO benford;

--
-- Name: benford_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: benford
--

ALTER SEQUENCE public.benford_id_seq OWNED BY public.benford.id;


--
-- Name: benford id; Type: DEFAULT; Schema: public; Owner: benford
--

ALTER TABLE ONLY public.benford ALTER COLUMN id SET DEFAULT nextval('public.benford_id_seq'::regclass);


--
-- Data for Name: benford; Type: TABLE DATA; Schema: public; Owner: benford
--

COPY public.benford (id, filename, contents, metadata) FROM stdin;
\.


--
-- Name: benford_id_seq; Type: SEQUENCE SET; Schema: public; Owner: benford
--

SELECT pg_catalog.setval('public.benford_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--
