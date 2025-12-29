import asyncio
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from .core.client import RiotClient, RiotClientConfig
from .core.types import Region

app = typer.Typer(help="RiotSkillIssue API Wrapper CLI")
console = Console()

@app.command()
def summoner(name: str, region: str = "na1", api_key: str = typer.Option(None, envvar="RIOT_API_KEY")):
    """Get summoner details by name."""
    
    async def _run():
        config = RiotClientConfig(api_key=api_key)
        async with RiotClient(config=config) as client:
            try:
                # Assuming simple name lookup still works or we use puuid if known
                # But spec removed get_by_name. Using get_by_account logic or similar?
                # Actually, summoner-v4 still has get_by_name in some regions but spec might hide it.
                # Let's assume we use get_by_puuid for safety if name lookup is deprecated, 
                # but CLI user wants name.
                # For this demo, let's use the account-v1 to get puuid then summoner.
                
                # Step 1: Account (Tagline needed)
                if "#" in name:
                    game_name, tag_line = name.split("#")
                else:
                    rprint("[red]Name must be format GameName#TagLine for Account V1 lookup[/red]")
                    return

                # Note: Account V1 is usually region 'americas', 'europe', etc.
                # We do a best effort mapping or ask user.
                # For simplicity, assume "americas" if region is na1/br1/etc.
                # This is complex, but let's try direct account lookup on 'americas' for NA.
                
                # Actually, let's just expose the raw method if available or specific flow.
                # Since get_by_name is gone from summoner_v4 in latest specs (replaced by account->puuid->summoner),
                # we do the Account flow.
                
                rprint(f"[bold blue]Fetching {game_name}#{tag_line}...[/bold blue]")
                
                # Account lookup (using americas as default cluster for simplicity in CLI)
                # In real app, map region->cluster.
                cluster = "americas" 
                
                account = await client.account.get_by_riot_id(region=cluster, gameName=game_name, tagLine=tag_line)
                puuid = account.puuid
                
                # Summoner lookup
                summ = await client.summoner.get_by_puuid(region=region, encryptedPUUID=puuid)
                
                table = Table(title=f"Summoner: {game_name}#{tag_line}")
                table.add_column("Level", style="magenta")
                table.add_column("PUUID", style="cyan", no_wrap=True)
                table.add_row(str(summ.summonerLevel), summ.puuid)
                
                console.print(table)
                
            except Exception as e:
                rprint(f"[red]Error: {e}[/red]")

    asyncio.run(_run())

@app.command()
def match(match_id: str, region: str = "americas", api_key: str = typer.Option(None, envvar="RIOT_API_KEY")):
    """Get match details."""
    async def _run():
        config = RiotClientConfig(api_key=api_key)
        async with RiotClient(config=config) as client:
            try:
                m = await client.match.get_match(region=region, matchId=match_id)
                rprint(f"[green]Match {match_id} loaded![/green]")
                rprint(f"Game Mode: {m.info.gameMode}")
                rprint(f"Duration: {m.info.gameDuration}s")
            except Exception as e:
                rprint(f"[red]Error: {e}[/red]")
                
    asyncio.run(_run())

def main():
    app()
