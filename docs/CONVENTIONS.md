# Conventions

## Naming
- Files: snake_case
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE

## Imports
- stdlib → third-party → local (enforced by ruff isort)

## Handler Pattern

async def handle_command(message: Message, storage: Storage) -> None:
    # 1. Parse input
    # 2. Validate
    # 3. Call storage
    # 4. Format and send response

## Testing Pattern

async def test_function_scenario(storage: Storage) -> None:
    result = await storage.add_application(user_id=123, company="Test", position="Dev")
    assert result.company == "Test"

## Commit Messages
- feat: new feature
- fix: bug fix
- test: adding/fixing tests
- docs: documentation
- chore: config, CI, infra
