-- Run this in the Supabase dashboard: SQL Editor -> New query -> paste -> Run
-- Safe to re-run: adds missing columns/policies without touching existing data.

create table if not exists plants (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    created_at timestamptz not null default now()
);

alter table plants add column if not exists status text not null default 'Unknown';
alter table plants add column if not exists description text default '';
alter table plants add column if not exists image_path text;
alter table plants add column if not exists risk numeric not null default 0;

alter table plants enable row level security;

-- Single-user desktop app using the anon key: allow full access.
-- Tighten this (e.g. require auth.uid()) if you add multi-user login later.
drop policy if exists "Allow anon full access to plants" on plants;
create policy "Allow anon full access to plants"
    on plants
    for all
    to anon
    using (true)
    with check (true);

-- Storage bucket for leaf/plant photos.
insert into storage.buckets (id, name, public)
values ('plant-images', 'plant-images', true)
on conflict (id) do nothing;

drop policy if exists "Allow anon full access to plant-images" on storage.objects;
create policy "Allow anon full access to plant-images"
    on storage.objects
    for all
    to anon
    using (bucket_id = 'plant-images')
    with check (bucket_id = 'plant-images');
