-- أسماء الطالبات لكل فصل (لصفحة «الطالبات» وجدول «الحضور» في لبيبة)
-- الصقي هذا الملف كاملاً في Supabase › SQL Editor ثم اضغطي Run (مرة واحدة)

create table if not exists public.students (
  id uuid primary key default gen_random_uuid(),
  grade_id text not null,                                              -- رمز الصف مثل m1 أو s2
  class_name text not null check (char_length(class_name) between 1 and 30),  -- الفصل مثل ١/أ
  name text not null check (char_length(name) between 1 and 80),
  sort int not null default 0,
  created_at timestamptz not null default now()
);
create index if not exists students_grade_class on public.students (grade_id, class_name);

-- المعلمة فقط تقرأ الجدول كاملاً وتعدّله
alter table public.students enable row level security;
drop policy if exists "students teacher" on public.students;
create policy "students teacher" on public.students for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());
grant select, insert, update, delete on public.students to authenticated;

-- الطالبة تحتاج قائمة فصول صفّها ثم أسماء فصلها فقط لتختار اسمها قبل الدرس
create or replace function public.roster_classes(g text)
returns setof text language sql stable security definer set search_path = public as $$
  select distinct class_name from public.students where grade_id = g order by 1;
$$;
create or replace function public.roster_names(g text, c text)
returns setof text language sql stable security definer set search_path = public as $$
  select name from public.students where grade_id = g and class_name = c order by sort, name;
$$;
grant execute on function public.roster_classes(text) to anon, authenticated;
grant execute on function public.roster_names(text, text) to anon, authenticated;
