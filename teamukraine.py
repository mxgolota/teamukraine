from flask import Flask, render_template
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import pandas as pd
import numpy as np

app = Flask(__name__)
dbconfig = read_db_config()

@app.route("/")
def index():
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    cursor.callproc("usp_stat_clubs_players_cnt")
    clubs_players_cnt = []
    for result in cursor.stored_results():
        for mid in result.fetchall():
            clubs_players_cnt.append(mid)
    cursor.close()
    return render_template("index.html", clubs_players_cnt=clubs_players_cnt)

@app.route("/teams")
def teams():
    return "Ololo!"

@app.route("/teams/<int:club_id>")
def club(club_id):
    conn = MySQLConnection(**dbconfig)
    info = conn.cursor()
    info.callproc("usp_club_info", [club_id])
    club_info = []
    for recordset in info.stored_results():
        for row in recordset:
            club_info.append(dict(zip(recordset.column_names, row)))
    info.close()

    matches = conn.cursor()
    matches.callproc("usp_club_matches", [club_id])
    club_matches = []
    for recordset in matches.stored_results():
        for row in recordset:
            club_matches.append(dict(zip(recordset.column_names, row)))
        matches.close()
    return render_template("club.html",
                           club_id=club_id,
                           club_info=club_info[0],
                           club_matches_reg=[x for x in club_matches if x['status'] == 'registration'],
                           club_matches_prog = [x for x in club_matches if x['status'] == 'in_progress'])

@app.route("/players")
def players():
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    cursor.callproc("usp_players_search")
    result = []
    for recordset in cursor.stored_results():
        for row in recordset:
            result.append(dict(zip(recordset.column_names, row)))
    cursor.close()
    return render_template("players.html", players=result)


@app.route("/tournaments/lcwl_u1600")
def lcwl_u1600():
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    cursor.callproc("usp_stat_lcwl_u1600")
    result = []
    for recordset in cursor.stored_results():
        for row in recordset:
            result.append(dict(zip(recordset.column_names, row)))
    cursor.close()

    tmp = pd.DataFrame(result)
    tmp = pd.pivot_table(tmp, columns='club_2', index='player_1', values='team1_player_score')\
        .reset_index()\
        .rename_axis(None, axis=1)
    # tmp.set_index('player_1', inplace=True)
    # tmp.reset_index(inplace=True)
    #tmp.reset_index(inplace=True)
    #tmp.columns = tmp.columns.get_level_values(0)
    tmp['Total'] = tmp[list(tmp.columns[1:])].sum(axis=1)
    rivals = tmp.columns[1:]
    tmp = tmp.sort_values(by=['Total'], ascending=False)

    return render_template("lcwl_best_players.html", tmp=tmp, rivals=rivals)


@app.route("/tournaments/lcwl_main")
def lcwl_main():
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    cursor.callproc("usp_stat_lcwl_main")
    result = []
    for recordset in cursor.stored_results():
        for row in recordset:
            result.append(dict(zip(recordset.column_names, row)))
    cursor.close()

    tmp = pd.DataFrame(result)
    tmp = pd.pivot_table(tmp, columns='club_2', index='player_1', values='team1_player_score')\
        .reset_index()\
        .rename_axis(None, axis=1)
    # tmp.set_index('player_1', inplace=True)
    # tmp.reset_index(inplace=True)
    #tmp.reset_index(inplace=True)
    #tmp.columns = tmp.columns.get_level_values(0)
    tmp['Total'] = tmp[list(tmp.columns[1:])].sum(axis=1)
    rivals = tmp.columns[1:]
    tmp = tmp.sort_values(by=['Total'], ascending=False)

    return render_template("lcwl_best_players.html", tmp=tmp, rivals=rivals)

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run(debug=True)
