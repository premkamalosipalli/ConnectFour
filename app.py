#!/usr/bin/env python

import asyncio

import websockets

import json

import logging
import itertools

from connect4 import PLAYER1, PLAYER2, Connect4

async def handler(websocket):
    # Initialize a Connect Four Game
    game = Connect4()

    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)

    async for message in websocket:
        # Parse incomming messagge
        event = json.loads(message)

        # Check for the correct event type
        if event["type"]=="play":
            column = event["column"]

        try:
            # Play the move and get the row
            row = game.play(player, column)
        except RuntimeError as exec:
            # Send an error message if the move is invalid
            event={
                "type":"error",
                "message":str(exec),
            }
            await websocket.send(json.dumps(event))
            continue

        # Send Play event to the client
        play_event={
            "type":"play",
            "player":player,
            "column":column,
            "row":row,
        }
        await websocket.send(json.dumps(play_event))

        # Check if there's a winner
        if game.winner is not None:
            win_event = {
                "type":"win",
                "player": game.winner,
            }
            await websocket.send(json.dumps(win_event))

        # Switch Players
        player = next(turns)

async def main():
    # Start the WebSocket server on port 8001
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())