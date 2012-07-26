-- Initialize the BiblioBox tables

create table formats (
       format_id integer primary key,
       format_name text,
       format_type text
);

insert into formats (format_name, format_type)
        values ('EPUB', 'application/epub+zip');
insert into formats (format_name, format_type)
        values ('PDF', 'application/pdf');
insert into formats (format_name, format_type)
       values ('JPEG', 'image/jpeg');

create table authors (
       author_id integer primary key,
       author_name text collate nocase,
       sort_name text collate nocase,
       uuid text not NULL,
       note text
);

create table works (
       work_id integer primary key,
       uuid text,
       sort_title text collate nocase,
       citation text,
       description text,
       cover text,
       cover_fmt integer references formats(format_id)
);

create table work_authors (
       work_id integer references works(work_id),
       author_id integer references authors(author_id)
);

create table books (
       id integer primary key,
       work_id integer references works(work_id),
       format_id integer references formats(format_id),
       filename text NOT NULL
);

create table tags (
       tag_id integer primary key,
       uuid text,
       tag_name text collate nocase
);

create table work_tags (
       work_id integer references works(work_id),
       tag_id integer references tags(tag_id)
);

create index author_index on authors(sort_name);

create index work_author_index on work_authors(work_id, author_id);

create index works_index on works(citation);

create index books_index on books(work_id);

create index work_tags_index on work_tags(work_id, tag_id);

create index tag_index on tags(tag_name);
