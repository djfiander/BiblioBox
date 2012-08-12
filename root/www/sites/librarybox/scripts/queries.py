from sys import stderr
import sqlite3

title_query = """SELECT au.author_name as author,
                        w.citation as title,
                        w.description as descr,
                        w.work_id as work_id,
                        w.uuid as uuid,
                        w.cover as cover,
                        cf.format_type as cover_fmt
                 FROM authors au, works w, work_authors wa, formats cf
                 WHERE w.work_id = wa.work_id
                   AND wa.author_id = au.author_id
                   AND cf.format_id = w.cover_fmt
                 ORDER BY w.sort_title"""

books_query = """SELECT f.format_type as ftype,
                        f.format_name as fmt_name,
                        b.filename as fname
                 FROM books b, formats f
                 WHERE b.work_id = ?
                   AND b.format_id = f.format_id
                 ORDER BY b.format_id"""

author_list_query = """SELECT au.uuid as uuid,
                              au.author_id as id,
	                      au.author_name as name,
                              count(wa.work_id) as titlecount
                       FROM authors au, work_authors wa
                       WHERE au.author_id = wa.author_id
                       GROUP BY wa.author_id
                       ORDER BY au.sort_name"""

author_info_query= """SELECT au.author_name as name,
                             au.uuid as uuid
                      FROM authors au
                      WHERE au.author_id = ?"""

author_works_query = """SELECT au.author_name as author,
                               w.citation as title,
                               w.uuid as uuid,
                               w.work_id as work_id,
                               w.description as descr,
                               w.cover as cover,
                               cf.format_type as cover_fmt
                        FROM authors au, work_authors wa, works w, formats cf
                        WHERE wa.author_id = ?
                          AND au.author_id = wa.author_id
                          AND w.work_id = wa.work_id
                          AND cf.format_id = w.cover_fmt
                        ORDER BY w.sort_title"""

# Returns iterator that returns all titles in the database
def titlelist(conn):
    for work in conn.execute(title_query):
        yield (work)

# Returns iterator that returns all formats available for
# single title
def booklist(conn, workid):
    qparm = (workid,)

    for book in conn.execute(books_query, qparm):
        yield book

def author_list(conn):
    for author in conn.execute(author_list_query):
        yield author

def author_info(conn, author_id):
      qparm = (author_id,)
      return conn.execute(author_info_query, qparm).fetchone()

def author_works(conn, author_id):
    qparm = (author_id,)
    for work in conn.execute(author_works_query, qparm):
        yield work
