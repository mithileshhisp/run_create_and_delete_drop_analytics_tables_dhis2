-- drop all analytics tables

DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
          AND tablename LIKE 'analytics_%'
    LOOP
        EXECUTE format(
            'DROP TABLE IF EXISTS public.%I CASCADE',
            r.tablename
        );
    END LOOP;
END $$;

-- list of analytics tables
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename LIKE 'analytics_%'
ORDER BY tablename;

-- TRUNCATE analytics table not drop
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
          AND tablename LIKE 'analytics_%'
    LOOP
        EXECUTE format(
            'TRUNCATE TABLE public.%I CASCADE',
            r.tablename
        );
    END LOOP;
END $$;