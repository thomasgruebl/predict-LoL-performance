create extension "uuid-ossp";

DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS matchup;
DROP TABLE IF EXISTS summoner;
DROP TABLE IF EXISTS summoner_match_rel;

CREATE TABLE public.match
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    match_id text COLLATE pg_catalog."default" NOT NULL,
    creation timestamp with time zone NOT NULL,
    game_version text COLLATE pg_catalog."default" NOT NULL,
    duration time without time zone,
    CONSTRAINT match_pkey PRIMARY KEY (id)
);

CREATE TABLE public.matchup
(
    summoner_id_1 uuid NOT NULL,
    summoner_id_2 uuid NOT NULL,
    champion_1 text COLLATE pg_catalog."default" NOT NULL,
    champion_2 text COLLATE pg_catalog."default" NOT NULL,
    champion_1_win boolean NOT NULL,
    champion_1_kills integer NOT NULL,
    champion_1_assists integer NOT NULL,
    champion_1_deaths integer NOT NULL,
    champion_2_kills integer NOT NULL,
    champion_2_assists integer NOT NULL,
    champion_2_deaths integer NOT NULL,
    match_id uuid,
    CONSTRAINT matchup_id PRIMARY KEY (summoner_id_1, summoner_id_2),
    CONSTRAINT match_id FOREIGN KEY (match_id)
        REFERENCES public.match (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE public.summoner
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    name text COLLATE pg_catalog."default" NOT NULL,
    puuid text COLLATE pg_catalog."default" NOT NULL,
    total_time_played double precision NOT NULL,
    CONSTRAINT summoner_pkey PRIMARY KEY (id)
);

CREATE TABLE public.summoner_match_rel
(
    summoner_id uuid NOT NULL,
    match_id uuid NOT NULL,
    CONSTRAINT summoner_match_id PRIMARY KEY (summoner_id, match_id)
);
