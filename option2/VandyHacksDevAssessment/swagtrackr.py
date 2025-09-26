import click
from typing import Optional
from db import (
    initialize_database,
    get_connection,
    create_or_update_item,
    set_item_quantity,
    list_items,
    delete_item,
    checkout_item,
)


@click.group()
def cli() -> None:
    """SwagTrackr - minimal inventory management CLI."""
    initialize_database()


@cli.command()
@click.argument("name", type=str)
@click.argument("quantity", type=int)
def add(name: str, quantity: int) -> None:
    """Add a new item or increase its quantity by QUANTITY."""
    with get_connection() as conn:
        item_id, new_qty = create_or_update_item(conn, name, quantity)
        click.echo(f"Added {quantity} of {name}. New total: {new_qty}")


@cli.command("restock")
@click.argument("name", type=str)
@click.argument("quantity", type=int)
def restock_cmd(name: str, quantity: int) -> None:
    """Increase quantity of an existing item by QUANTITY."""
    with get_connection() as conn:
        item_id, new_qty = create_or_update_item(conn, name, quantity)
        click.echo(f"Restocked {quantity} of {name}. New total: {new_qty}")


@cli.command("set-qty")
@click.argument("name", type=str)
@click.argument("quantity", type=int)
def set_qty_cmd(name: str, quantity: int) -> None:
    """Set item quantity to QUANTITY (can create item)."""
    with get_connection() as conn:
        item_id, new_qty = set_item_quantity(conn, name, quantity)
        click.echo(f"Set {name} to {new_qty}")


@cli.command()
@click.argument("name", type=str)
@click.argument("amount", type=int)
@click.option("--to", "recipient", type=str, default=None, help="Recipient name or identifier")
def checkout(name: str, amount: int, recipient: Optional[str]) -> None:
    """Check out AMOUNT of NAME to recipient (optional)."""
    with get_connection() as conn:
        try:
            item_id, new_qty = checkout_item(conn, name, amount, recipient)
        except ValueError as e:
            click.echo(f"Error: {e}")
            raise SystemExit(1)
        click.echo(f"Checked out {amount} of {name}. Remaining: {new_qty}")


@cli.command()
def list() -> None:  # type: ignore[override]
    """List all items with quantities."""
    with get_connection() as conn:
        rows = list_items(conn)
        if not rows:
            click.echo("Inventory is empty.")
            return
        click.echo("Inventory:")
        for _id, name, qty in rows:
            click.echo(f"- {name}: {qty}")


@cli.command()
@click.argument("name", type=str)
def delete(name: str) -> None:  # type: ignore[override]
    """Delete an item by NAME."""
    with get_connection() as conn:
        ok = delete_item(conn, name)
        if ok:
            click.echo(f"Deleted {name}")
        else:
            click.echo("Item not found")
            raise SystemExit(1)


if __name__ == "__main__":
    cli()
