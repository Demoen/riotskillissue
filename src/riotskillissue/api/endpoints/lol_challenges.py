# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Lol_challengesApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_all_challenge_configs(
        self,
        region: str,
        
    ) -> List[lol_challenges_v1_ChallengeConfigInfoDto]:
        """
        List of all basic challenge configuration information (includes all translations for names and descriptions)
        """
        path = "/lol/challenges/v1/challenges/config"
        # Replace path params
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(List[lol_challenges_v1_ChallengeConfigInfoDto]).validate_python(response.json())
        
    
    async def get_all_challenge_percentiles(
        self,
        region: str,
        
    ) -> Dict[str, Dict[str, float]]:
        """
        Map of level to percentile of players who have achieved it - keys: ChallengeId -> Season -> Level -> percentile of players who achieved it
        """
        path = "/lol/challenges/v1/challenges/percentiles"
        # Replace path params
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(Dict[str, Dict[str, float]]).validate_python(response.json())
        
    
    async def get_challenge_configs(
        self,
        region: str,
        
        challengeId: int,
        
    ) -> lol_challenges_v1_ChallengeConfigInfoDto:
        """
        Get challenge configuration (REST)
        """
        path = "/lol/challenges/v1/challenges/{challengeId}/config"
        # Replace path params
        
        path = path.replace("{" + "challengeId" + "}", str(challengeId))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(lol_challenges_v1_ChallengeConfigInfoDto).validate_python(response.json())
        
    
    async def get_challenge_leaderboards(
        self,
        region: str,
        
        challengeId: int,
        
        level: str,
        
        limit: int = None,
        
    ) -> List[lol_challenges_v1_ApexPlayerInfoDto]:
        """
        Return top players for each level. Level must be MASTER, GRANDMASTER or CHALLENGER.
        """
        path = "/lol/challenges/v1/challenges/{challengeId}/leaderboards/by-level/{level}"
        # Replace path params
        
        path = path.replace("{" + "challengeId" + "}", str(challengeId))
        
        path = path.replace("{" + "level" + "}", str(level))
        

        # Query params
        params = {
            
            "limit": limit,
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(List[lol_challenges_v1_ApexPlayerInfoDto]).validate_python(response.json())
        
    
    async def get_challenge_percentiles(
        self,
        region: str,
        
        challengeId: int,
        
    ) -> Dict[str, float]:
        """
        Map of level to percentile of players who have achieved it
        """
        path = "/lol/challenges/v1/challenges/{challengeId}/percentiles"
        # Replace path params
        
        path = path.replace("{" + "challengeId" + "}", str(challengeId))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(Dict[str, float]).validate_python(response.json())
        
    
    async def get_player_data(
        self,
        region: str,
        
        puuid: str,
        
    ) -> lol_challenges_v1_PlayerInfoDto:
        """
        Returns player information with list of all progressed challenges (REST)
        """
        path = "/lol/challenges/v1/player-data/{puuid}"
        # Replace path params
        
        path = path.replace("{" + "puuid" + "}", str(puuid))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(lol_challenges_v1_PlayerInfoDto).validate_python(response.json())
        
    