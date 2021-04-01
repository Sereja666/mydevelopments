import pyad.adquery


def checkname():
    dict_name = []
    q = pyad.adquery.ADQuery()

    q.execute_query(
        attributes=["cn", "description"],
        where_clause="objectClass = '*'",
        base_dn="OU=!new, OU=ksc, DC=ava, DC=corp"
    )

    for row in q.get_results():
        dict_name.append(row["cn"])

checkname()