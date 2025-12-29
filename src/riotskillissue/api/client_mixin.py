# Generated Code. Do not edit.
from riotskillissue.core.http import HttpClient

from riotskillissue.api.endpoints.lol_challenges import Lol_challengesApi

from riotskillissue.api.endpoints.champion_mastery import Champion_masteryApi

from riotskillissue.api.endpoints.clash import ClashApi

from riotskillissue.api.endpoints.league_exp import League_expApi

from riotskillissue.api.endpoints.league import LeagueApi

from riotskillissue.api.endpoints.match import MatchApi

from riotskillissue.api.endpoints.champion import ChampionApi

from riotskillissue.api.endpoints.lol_rso_match import Lol_rso_matchApi

from riotskillissue.api.endpoints.spectator_tft import Spectator_tftApi

from riotskillissue.api.endpoints.spectator import SpectatorApi

from riotskillissue.api.endpoints.lol_status import Lol_statusApi

from riotskillissue.api.endpoints.summoner import SummonerApi

from riotskillissue.api.endpoints.tournament_stub import Tournament_stubApi

from riotskillissue.api.endpoints.tournament import TournamentApi

from riotskillissue.api.endpoints.lor_deck import Lor_deckApi

from riotskillissue.api.endpoints.lor_inventory import Lor_inventoryApi

from riotskillissue.api.endpoints.lor_match import Lor_matchApi

from riotskillissue.api.endpoints.lor_ranked import Lor_rankedApi

from riotskillissue.api.endpoints.lor_status import Lor_statusApi

from riotskillissue.api.endpoints.riftbound_content import Riftbound_contentApi

from riotskillissue.api.endpoints.account import AccountApi

from riotskillissue.api.endpoints.tft_league import Tft_leagueApi

from riotskillissue.api.endpoints.tft_match import Tft_matchApi

from riotskillissue.api.endpoints.tft_status import Tft_statusApi

from riotskillissue.api.endpoints.tft_summoner import Tft_summonerApi

from riotskillissue.api.endpoints.val_console_ranked import Val_console_rankedApi

from riotskillissue.api.endpoints.val_content import Val_contentApi

from riotskillissue.api.endpoints.val_console_match import Val_console_matchApi

from riotskillissue.api.endpoints.val_match import Val_matchApi

from riotskillissue.api.endpoints.val_ranked import Val_rankedApi

from riotskillissue.api.endpoints.val_status import Val_statusApi


class GeneratedClientMixin:
    def __init__(self, http: HttpClient):
        
        self.lol_challenges = Lol_challengesApi(http)
        
        self.champion_mastery = Champion_masteryApi(http)
        
        self.clash = ClashApi(http)
        
        self.league_exp = League_expApi(http)
        
        self.league = LeagueApi(http)
        
        self.match = MatchApi(http)
        
        self.champion = ChampionApi(http)
        
        self.lol_rso_match = Lol_rso_matchApi(http)
        
        self.spectator_tft = Spectator_tftApi(http)
        
        self.spectator = SpectatorApi(http)
        
        self.lol_status = Lol_statusApi(http)
        
        self.summoner = SummonerApi(http)
        
        self.tournament_stub = Tournament_stubApi(http)
        
        self.tournament = TournamentApi(http)
        
        self.lor_deck = Lor_deckApi(http)
        
        self.lor_inventory = Lor_inventoryApi(http)
        
        self.lor_match = Lor_matchApi(http)
        
        self.lor_ranked = Lor_rankedApi(http)
        
        self.lor_status = Lor_statusApi(http)
        
        self.riftbound_content = Riftbound_contentApi(http)
        
        self.account = AccountApi(http)
        
        self.tft_league = Tft_leagueApi(http)
        
        self.tft_match = Tft_matchApi(http)
        
        self.tft_status = Tft_statusApi(http)
        
        self.tft_summoner = Tft_summonerApi(http)
        
        self.val_console_ranked = Val_console_rankedApi(http)
        
        self.val_content = Val_contentApi(http)
        
        self.val_console_match = Val_console_matchApi(http)
        
        self.val_match = Val_matchApi(http)
        
        self.val_ranked = Val_rankedApi(http)
        
        self.val_status = Val_statusApi(http)
        