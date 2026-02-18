# Generated Code. Do not edit.
from riotskillissue.core.http import HttpClient

from riotskillissue.api.endpoints.lol_challenges import LolChallengesApi

from riotskillissue.api.endpoints.champion_mastery import ChampionMasteryApi

from riotskillissue.api.endpoints.clash import ClashApi

from riotskillissue.api.endpoints.league_exp import LeagueExpApi

from riotskillissue.api.endpoints.league import LeagueApi

from riotskillissue.api.endpoints.match import MatchApi

from riotskillissue.api.endpoints.champion import ChampionApi

from riotskillissue.api.endpoints.lol_rso_match import LolRsoMatchApi

from riotskillissue.api.endpoints.spectator_tft import SpectatorTftApi

from riotskillissue.api.endpoints.spectator import SpectatorApi

from riotskillissue.api.endpoints.lol_status import LolStatusApi

from riotskillissue.api.endpoints.summoner import SummonerApi

from riotskillissue.api.endpoints.tournament_stub import TournamentStubApi

from riotskillissue.api.endpoints.tournament import TournamentApi

from riotskillissue.api.endpoints.lor_deck import LorDeckApi

from riotskillissue.api.endpoints.lor_inventory import LorInventoryApi

from riotskillissue.api.endpoints.lor_match import LorMatchApi

from riotskillissue.api.endpoints.lor_ranked import LorRankedApi

from riotskillissue.api.endpoints.lor_status import LorStatusApi

from riotskillissue.api.endpoints.riftbound_content import RiftboundContentApi

from riotskillissue.api.endpoints.account import AccountApi

from riotskillissue.api.endpoints.tft_league import TftLeagueApi

from riotskillissue.api.endpoints.tft_match import TftMatchApi

from riotskillissue.api.endpoints.tft_status import TftStatusApi

from riotskillissue.api.endpoints.tft_summoner import TftSummonerApi

from riotskillissue.api.endpoints.val_console_ranked import ValConsoleRankedApi

from riotskillissue.api.endpoints.val_content import ValContentApi

from riotskillissue.api.endpoints.val_console_match import ValConsoleMatchApi

from riotskillissue.api.endpoints.val_match import ValMatchApi

from riotskillissue.api.endpoints.val_ranked import ValRankedApi

from riotskillissue.api.endpoints.val_status import ValStatusApi


class GeneratedClientMixin:
    def __init__(self, http: HttpClient):
        
        self.lol_challenges = LolChallengesApi(http)
        
        self.champion_mastery = ChampionMasteryApi(http)
        
        self.clash = ClashApi(http)
        
        self.league_exp = LeagueExpApi(http)
        
        self.league = LeagueApi(http)
        
        self.match = MatchApi(http)
        
        self.champion = ChampionApi(http)
        
        self.lol_rso_match = LolRsoMatchApi(http)
        
        self.spectator_tft = SpectatorTftApi(http)
        
        self.spectator = SpectatorApi(http)
        
        self.lol_status = LolStatusApi(http)
        
        self.summoner = SummonerApi(http)
        
        self.tournament_stub = TournamentStubApi(http)
        
        self.tournament = TournamentApi(http)
        
        self.lor_deck = LorDeckApi(http)
        
        self.lor_inventory = LorInventoryApi(http)
        
        self.lor_match = LorMatchApi(http)
        
        self.lor_ranked = LorRankedApi(http)
        
        self.lor_status = LorStatusApi(http)
        
        self.riftbound_content = RiftboundContentApi(http)
        
        self.account = AccountApi(http)
        
        self.tft_league = TftLeagueApi(http)
        
        self.tft_match = TftMatchApi(http)
        
        self.tft_status = TftStatusApi(http)
        
        self.tft_summoner = TftSummonerApi(http)
        
        self.val_console_ranked = ValConsoleRankedApi(http)
        
        self.val_content = ValContentApi(http)
        
        self.val_console_match = ValConsoleMatchApi(http)
        
        self.val_match = ValMatchApi(http)
        
        self.val_ranked = ValRankedApi(http)
        
        self.val_status = ValStatusApi(http)
        