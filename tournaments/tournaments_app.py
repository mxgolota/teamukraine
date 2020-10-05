from flask import Blueprint, render_template
from database import engine
import numpy as np
import pandas as pd

tournaments_bp = Blueprint('tournaments_bp', __name__, template_folder='templates', url_prefix='/tournaments')


@tournaments_bp.route('/')
def index():
    return render_template('tournaments.html')


@tournaments_bp.route("/lcwl_u1600")
def lcwl_u1600():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_lcwl_u1600")
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    max_points = pd.DataFrame(result, columns=columns)
    points = pd.pivot_table(points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_score') \
        .reset_index()
    cols = [('player_1', ''), ('chess_blitz_rating', '')] + sorted(list(points.columns)[2:], key=lambda x: x[1])
    points = points.reindex(columns=cols).reset_index(drop=True)

    points['Total'] = points[list(points.columns[2:])].sum(axis=1)
    rivals = points.columns[2:]
    points = points.sort_values(by=['Total'], ascending=False)

    max_points = pd.pivot_table(max_points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                                values='team1_player_max_possible_score').reset_index()
    max_points = max_points.reindex(columns=cols).reset_index(drop=True)

    max_points['Total_max'] = max_points[list(max_points.columns[2:])].sum(axis=1)

    points = pd.merge(points, max_points[['Total_max', 'player_1']], on='player_1', how='left')
    points['points_percentage'] = 100 * points['Total'] / points['Total_max']
    points = points.sort_values(by=['Total', 'points_percentage'], ascending=False)
    points['Place'] = np.arange(1, len(points) + 1)

    return render_template("lcwl_best_players.html", points=points, rivals=rivals)


@tournaments_bp.route("/lcwl_main")
def lcwl_main():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_lcwl_main")
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    max_points = pd.DataFrame(result, columns=columns)
    points = pd.pivot_table(points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_score') \
        .reset_index()
    cols = [('player_1', ''), ('chess_blitz_rating', '')] + sorted(list(points.columns)[2:], key=lambda x: x[1])
    points = points.reindex(columns=cols).reset_index(drop=True)

    points['Total'] = points[list(points.columns[2:])].sum(axis=1)
    rivals = points.columns[2:]
    points = points.sort_values(by=['Total'], ascending=False)

    max_points = pd.pivot_table(max_points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_max_possible_score').reset_index()
    max_points = max_points.reindex(columns=cols).reset_index(drop=True)

    max_points['Total_max'] = max_points[list(max_points.columns[2:])].sum(axis=1)

    points = pd.merge(points, max_points[['Total_max', 'player_1']], on='player_1', how='left')
    points['points_percentage'] = 100*points['Total']/points['Total_max']
    points = points.sort_values(by=['Total', 'points_percentage'], ascending=False)
    points['Place'] = np.arange(1, len(points) + 1)

    return render_template("lcwl_best_players.html", points=points, rivals=rivals)


@tournaments_bp.route("/lcwl_s5_main")
def lcwl_s5_main():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_lcwl_s5_main")
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    max_points = pd.DataFrame(result, columns=columns)
    points = pd.pivot_table(points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_score') \
        .reset_index()
    cols = [('player_1', ''), ('chess_blitz_rating', '')] + sorted(list(points.columns)[2:], key=lambda x: x[1])
    points = points.reindex(columns=cols).reset_index(drop=True)

    points['Total'] = points[list(points.columns[2:])].sum(axis=1)
    rivals = points.columns[2:]
    points = points.sort_values(by=['Total'], ascending=False)

    max_points = pd.pivot_table(max_points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_max_possible_score').reset_index()
    max_points = max_points.reindex(columns=cols).reset_index(drop=True)

    max_points['Total_max'] = max_points[list(max_points.columns[2:])].sum(axis=1)

    points = pd.merge(points, max_points[['Total_max', 'player_1']], on='player_1', how='left')
    points['points_percentage'] = 100*points['Total']/points['Total_max']
    points = points.sort_values(by=['Total', 'points_percentage'], ascending=False)
    points['Place'] = np.arange(1, len(points) + 1)

    return render_template("lcwl_best_players.html", points=points, rivals=rivals)


@tournaments_bp.route("/lcwl_s5_u1600")
def lcwl_s5_u1600():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_lcwl_s5_u1600")
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    max_points = pd.DataFrame(result, columns=columns)
    points = pd.pivot_table(points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_score') \
        .reset_index()
    cols = [('player_1', ''), ('chess_blitz_rating', '')] + sorted(list(points.columns)[2:], key=lambda x: x[1])
    points = points.reindex(columns=cols).reset_index(drop=True)

    points['Total'] = points[list(points.columns[2:])].sum(axis=1)
    rivals = points.columns[2:]
    points = points.sort_values(by=['Total'], ascending=False)

    max_points = pd.pivot_table(max_points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_max_possible_score').reset_index()
    max_points = max_points.reindex(columns=cols).reset_index(drop=True)

    max_points['Total_max'] = max_points[list(max_points.columns[2:])].sum(axis=1)

    points = pd.merge(points, max_points[['Total_max', 'player_1']], on='player_1', how='left')
    points['points_percentage'] = 100*points['Total']/points['Total_max']
    points = points.sort_values(by=['Total', 'points_percentage'], ascending=False)
    points['Place'] = np.arange(1, len(points) + 1)

    return render_template("lcwl_best_players.html", points=points, rivals=rivals)


@tournaments_bp.route("/ucc2019")
def ucc2019():
    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2019_best_players")
        best_players_result = [row for row in result]
        best_players_columns = result.keys()

    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2019_rounds")
        rounds_result = [row for row in result]
        rounds_result_columns = result.keys()

    best_players = pd.DataFrame(best_players_result, columns=best_players_columns)
    rounds = pd.DataFrame(rounds_result,columns=rounds_result_columns)
    first_teams = rounds[['round_id', 'match_id', 'team1_name', 'team1_result', 'team2_name']]
    first_teams = first_teams.rename(columns={"team1_name": "team_name", "team1_result": "team_result", "team2_name": "opponent_name"})
    second_teams = rounds[['round_id', 'match_id', 'team2_name', 'team2_result', 'team1_name']]
    second_teams = second_teams.rename(columns={"team2_name": "team_name", "team2_result": "team_result", "team1_name": "opponent_name"})
    tournament_table = pd.concat([first_teams, second_teams]).reset_index()

    tournament_table = pd.pivot_table(tournament_table, columns=['opponent_name'], index=['team_name'], values='team_result').reset_index()

    tournament_table['Загалом'] = tournament_table.sum(axis=1)
    tournament_table.reset_index(inplace=True)
    tournament_table.sort_values(by=['Загалом'], ascending=False, inplace=True)

    return render_template("ucc2019.html", best_players=best_players, rounds=rounds, tournament_table=tournament_table)


@tournaments_bp.route("/ucc2019_bullet_rapid")
def ucc2019_bullet_rapid():
    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2019_rapid_bullet_best_player")
        best_players_result = [row for row in result]
        best_players_columns = result.keys()

    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2019_rapid_bullet_rounds")
        rounds_result = [row for row in result]
        rounds_result_columns = result.keys()

    best_players = pd.DataFrame(best_players_result, columns=best_players_columns)
    rounds = pd.DataFrame(rounds_result, columns=rounds_result_columns)

    groupA_rounds = rounds.loc[rounds['team1_id'].isin([84300, 42800, 67918, 57502, 71728, 52452])
                               & rounds['round_id'].isin([1, 2, 3, 4, 5])]
    groupB_rounds = rounds.loc[rounds['team1_id'].isin([71066, 42164, 84302, 27634, 61104, 72704])
                               & rounds['round_id'].isin([1, 2, 3, 4, 5])]

    groupA_first_teams = groupA_rounds[['round_id', 'match_id', 'team1_name', 'team1_result', 'team2_name']]
    groupA_first_teams = groupA_first_teams.rename(columns={"team1_name": "team_name", "team1_result": "team_result", "team2_name": "opponent_name"})
    groupA_second_teams = groupA_rounds[['round_id', 'match_id', 'team2_name', 'team2_result', 'team1_name']]
    groupA_second_teams = groupA_second_teams.rename(columns={"team2_name": "team_name", "team2_result": "team_result", "team1_name": "opponent_name"})
    groupA_tournament_table = pd.concat([groupA_first_teams, groupA_second_teams]).reset_index()

    groupA_tournament_table = pd.pivot_table(groupA_tournament_table, columns=['opponent_name'], index=['team_name'], values='team_result', aggfunc='sum').reset_index()

    groupA_tournament_table['Загалом'] = groupA_tournament_table.sum(axis=1)
    groupA_tournament_table.reset_index(inplace=True)
    groupA_tournament_table.sort_values(by=['Загалом'], ascending=False, inplace=True)

    groupB_first_teams = groupB_rounds[['round_id', 'match_id', 'team1_name', 'team1_result', 'team2_name']]
    groupB_first_teams = groupB_first_teams.rename(
        columns={"team1_name": "team_name", "team1_result": "team_result", "team2_name": "opponent_name"})
    groupB_second_teams = groupB_rounds[['round_id', 'match_id', 'team2_name', 'team2_result', 'team1_name']]
    groupB_second_teams = groupB_second_teams.rename(
        columns={"team2_name": "team_name", "team2_result": "team_result", "team1_name": "opponent_name"})
    groupB_tournament_table = pd.concat([groupB_first_teams, groupB_second_teams]).reset_index()

    groupB_tournament_table = pd.pivot_table(groupB_tournament_table, columns=['opponent_name'], index=['team_name'],
                                             values='team_result', aggfunc='sum').reset_index()

    groupB_tournament_table['Загалом'] = groupB_tournament_table.sum(axis=1)
    groupB_tournament_table.reset_index(inplace=True)
    groupB_tournament_table.sort_values(by=['Загалом'], ascending=False, inplace=True)

    return render_template("ucc2019_bullet_rapid.html", best_players=best_players, rounds=rounds,
                           groupA_tournament_table=groupA_tournament_table,
                           groupB_tournament_table=groupB_tournament_table)


@tournaments_bp.route("/ucc2020_daily")
def ucc2020_daily():
    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2020daily_live_standings")
        live_standings_result = [row for row in result]
        live_standings_columns = result.keys()
    live_standings = pd.DataFrame(live_standings_result, columns=live_standings_columns)

    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2020daily_rounds")
        rounds_result = [row for row in result]
        rounds_columns = result.keys()
    rounds = pd.DataFrame(rounds_result, columns=rounds_columns)
    rounds_list = rounds['round_id'].unique().tolist()

    return render_template("ucc2020_daily.html", live_standings=live_standings, rounds=rounds, rounds_list=rounds_list)


@tournaments_bp.route("/green_chess_cup_3_4_grade")
def green_chess_cup_3_4_grade():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_marathon_tournament_table (%s)", (1, ))
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    rounds = sorted(points['round_id'].unique())

    points = pd.pivot_table(points, columns=['round_id'], index=['username'], values=['points', 'tie_break'],
                            aggfunc='sum') \
        .reset_index()
    points['Загалом'] = points['points'].sum(axis=1)
    points['КБ'] = points['tie_break'].sum(axis=1)
    points = points.sort_values(by=['Загалом', 'КБ'], ascending=(False, False)).reset_index()
    points['rnk'] = points['КБ'].index + 1
    points = points.fillna('')

    return render_template("green_chess_cup_marathon.html", points=points, rounds=rounds)


@tournaments_bp.route("/green_chess_cup_1_2_grade")
def green_chess_cup_1_2_grade():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_marathon_tournament_table (%s)", (2, ))
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    rounds = sorted(points['round_id'].unique())

    points = pd.pivot_table(points, columns=['round_id'], index=['username'], values=['points', 'tie_break'],
                            aggfunc='sum') \
        .reset_index()
    points['Загалом'] = points['points'].sum(axis=1)
    points['КБ'] = points['tie_break'].sum(axis=1)
    points = points.sort_values(by=['Загалом', 'КБ'], ascending=(False, False)).reset_index()
    points['rnk'] = points['КБ'].index + 1
    points = points.fillna('')

    return render_template("green_chess_cup_marathon.html", points=points, rounds=rounds)


@tournaments_bp.route("/green_chess_cup_1plus_grade")
def green_chess_cup_1plus_grade():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_marathon_tournament_table (%s)", (3, ))
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    rounds = sorted(points['round_id'].unique())

    points = pd.pivot_table(points, columns=['round_id'], index=['username'], values=['points', 'tie_break'], aggfunc='sum') \
        .reset_index()
    points['Загалом'] = points['points'].sum(axis=1)
    points['КБ'] = points['tie_break'].sum(axis=1)
    points = points.sort_values(by=['Загалом', 'КБ'], ascending=(False, False)).reset_index()
    points['rnk'] = points['КБ'].index + 1
    points = points.fillna('')

    return render_template("green_chess_cup_marathon.html", points=points, rounds=rounds)


@tournaments_bp.route("/ucc2020_blitz")
def ucc2020_blitz():
    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2020_blitz_best_players")
        best_players_result = [row for row in result]
        best_players_columns = result.keys()

    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2020_blitz_rounds")
        rounds_result = [row for row in result]
        rounds_result_columns = result.keys()

    best_players = pd.DataFrame(best_players_result, columns=best_players_columns)
    rounds = pd.DataFrame(rounds_result, columns=rounds_result_columns)
    first_teams = rounds[['round_id', 'match_id', 'team1_name', 'team1_result', 'team2_name']]
    first_teams = first_teams.rename(columns={"team1_name": "team_name", "team1_result": "team_result", "team2_name": "opponent_name"})
    second_teams = rounds[['round_id', 'match_id', 'team2_name', 'team2_result', 'team1_name']]
    second_teams = second_teams.rename(columns={"team2_name": "team_name", "team2_result": "team_result", "team1_name": "opponent_name"})
    tournament_table = pd.concat([first_teams, second_teams]).reset_index()

    tournament_table = pd.pivot_table(tournament_table, columns=['opponent_name'], index=['team_name'], values='team_result').reset_index()

    tournament_table['Загалом'] = tournament_table.sum(axis=1)
    tournament_table.reset_index(inplace=True)
    tournament_table.sort_values(by=['Загалом'], ascending=False, inplace=True)

    return render_template("ucc2019.html", best_players=best_players, rounds=rounds, tournament_table=tournament_table)


@tournaments_bp.route("/<tournament_id>")
def ucc_tournament(tournament_id):

    if int(tournament_id) in (11, 15):
        with engine.connect() as conn:
            tmp = conn.execute("call usp_stat_lcwl_bestplayers ({0})".format(tournament_id))
            result = [row for row in tmp]
            columns = tmp.keys()

        points = pd.DataFrame(result, columns=columns)
        max_points = pd.DataFrame(result, columns=columns)
        points = pd.pivot_table(points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                                values='team1_player_score') \
            .reset_index()
        cols = [('player_1', ''), ('chess_blitz_rating', '')] + sorted(list(points.columns)[2:], key=lambda x: x[1])
        points = points.reindex(columns=cols).reset_index(drop=True)

        points['Total'] = points[list(points.columns[2:])].sum(axis=1)
        rivals = points.columns[2:]
        points = points.sort_values(by=['Total'], ascending=False)

        max_points = pd.pivot_table(max_points, columns=['club_2', 'round_id'],
                                    index=['player_1', 'chess_blitz_rating'],
                                    values='team1_player_max_possible_score').reset_index()
        max_points = max_points.reindex(columns=cols).reset_index(drop=True)

        max_points['Total_max'] = max_points[list(max_points.columns[2:])].sum(axis=1)

        points = pd.merge(points, max_points[['Total_max', 'player_1']], on='player_1', how='left')
        points['points_percentage'] = 100 * points['Total'] / points['Total_max']
        points = points.sort_values(by=['Total', 'points_percentage'], ascending=False)
        points['Place'] = np.arange(1, len(points) + 1)

        return render_template("lcwl_best_players.html", points=points, rivals=rivals)

    else:
        with engine.connect() as conn:
            result = conn.execute("call usp_stat_ucc_best_players ({0})".format(tournament_id))
            best_players_result = [row for row in result]
            best_players_columns = result.keys()

        with engine.connect() as conn:
            result = conn.execute("call usp_stat_ucc_rounds ({0})".format(tournament_id))
            rounds_result = [row for row in result]
            rounds_result_columns = result.keys()

        best_players = pd.DataFrame(best_players_result, columns=best_players_columns)
        rounds = pd.DataFrame(rounds_result, columns=rounds_result_columns)
        first_teams = rounds[['round_id', 'match_id', 'team1_name', 'team1_result', 'team2_name']]
        first_teams = first_teams.rename(columns={"team1_name": "team_name", "team1_result": "team_result", "team2_name": "opponent_name"})
        second_teams = rounds[['round_id', 'match_id', 'team2_name', 'team2_result', 'team1_name']]
        second_teams = second_teams.rename(columns={"team2_name": "team_name", "team2_result": "team_result", "team1_name": "opponent_name"})
        tournament_table = pd.concat([first_teams, second_teams]).reset_index()

        tournament_table = pd.pivot_table(tournament_table, columns=['opponent_name'], index=['team_name'], values='team_result').reset_index()

        tournament_table['Загалом'] = tournament_table.sum(axis=1)
        tournament_table.reset_index(inplace=True)
        tournament_table.sort_values(by=['Загалом'], ascending=False, inplace=True)

        return render_template("ucc2019.html", best_players=best_players, rounds=rounds, tournament_table=tournament_table)
