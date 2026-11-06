-- SVI website enquiries. Run once in Supabase > SQL Editor.
-- Safe to re-run: it only creates what is missing.

create table if not exists public.enquiries (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text not null check (char_length(name) between 2 and 100),
  email text not null check (char_length(email) <= 254),
  phone text not null check (char_length(phone) between 7 and 30),
  company text not null default '' check (char_length(company) <= 150),
  panel_type text not null default '' check (char_length(panel_type) <= 60),
  message text not null check (char_length(message) between 20 and 5000),
  consent_at timestamptz not null default now(),
  status text not null default 'new' check (status in ('new', 'contacted', 'closed')),
  notes text not null default ''
);

-- For projects created from the earlier schema (adds the new columns).
alter table public.enquiries add column if not exists panel_type text not null default '' check (char_length(panel_type) <= 60);
alter table public.enquiries add column if not exists notes text not null default '';

create index if not exists enquiries_created_at_idx on public.enquiries (created_at desc);

-- Row-level security on, with no public policies: browsers can never read or
-- write this table. Only the website's server function (secret key) can.
alter table public.enquiries enable row level security;
revoke all on public.enquiries from anon, authenticated;
grant select, insert on public.enquiries to service_role;
