<script>
	import { onMount } from 'svelte';
	import { confetti } from '@neoconfetti/svelte';
	import { reduced_motion } from './reduced-motion';
	import { Game } from './game';

	let game;

	let guesses = ['', '', '', '', '', ''];
	let answers = [];
	let answer = '';
	let won = false;
	let lost = false;
	let badGuess = false;

	let i = 0; // current guess index
	$: submittable = guesses[i]?.length === 5;

	let classnames = {};
	let description = {};

	onMount(() => {
		start_new_game();
	});

	function start_new_game() {
		game = new Game();
		guesses = ['', '', '', '', '', ''];
		answers = [];
		answer = game.answer;
		won = false;
		lost = false;
		badGuess = false;
		i = 0;
		update_classnames();
	}

	function update_classnames() {
		classnames = {};
		description = {};

		answers.forEach((answer_row, i) => {
			const guess = guesses[i];

			for (let i = 0; i < 5; i += 1) {
				const letter = guess[i];

				if (answer_row[i] === 'x') {
					classnames[letter] = 'exact';
					description[letter] = 'correct';
				} else if (!classnames[letter]) {
					classnames[letter] = answer_row[i] === 'c' ? 'close' : 'missing';
					description[letter] = answer_row[i] === 'c' ? 'present' : 'absent';
				}
			}
		});
	}

	function handle_enter() {
		if (!submittable) return;

		const valid = game.enter(guesses[i].split(''));

		if (!valid) {
			badGuess = true;
			setTimeout(() => (badGuess = false), 500);
			return;
		}

		answers = game.answers;
		won = game.answers.at(-1) === 'xxxxx';
		lost = !won && game.answers.length >= 6;
		i = won || lost ? -1 : game.answers.length;

		update_classnames();
	}

	function handle_keyboard_update(event) {
		if (won || lost) return;
		const key = (event.target).getAttribute('data-key');

		if (key === 'backspace') {
			guesses[i] = guesses[i].slice(0, -1);
			if (badGuess) badGuess = false;
		} else if (guesses[i].length < 5) {
			guesses[i] += key;
		}
	}

	function handle_keydown(event) {
		if (event.metaKey || won || lost) return;

		if (event.key === 'Enter') {
			handle_enter();
			return;
		}

		document
			.querySelector(`[data-key="${event.key}" i]`)
			?.dispatchEvent(new MouseEvent('click', { cancelable: true }));
	}
</script>

<svelte:window on:keydown={handle_keydown} />

<svelte:head>
	<title>Sverdle</title>
	<meta name="description" content="A Wordle clone written in SvelteKit" />
</svelte:head>

<h1 class="visually-hidden">Sverdle</h1>

<div>
	<a class="how-to-play" href="/how-to-play">How to play</a>

	<div class="grid" class:playing={!won} class:bad-guess={badGuess}>
		{#each Array.from(Array(6).keys()) as row (row)}
			{@const current = row === i}
			<h2 class="visually-hidden">Row {row + 1}</h2>
			<div class="row" class:current>
				{#each Array.from(Array(5).keys()) as column (column)}
					{@const answer = answers[row]?.[column]}
					{@const value = guesses[row]?.[column] ?? ''}
					{@const selected = current && column === guesses[row].length}
					{@const exact = answer === 'x'}
					{@const close = answer === 'c'}
					{@const missing = answer === '_'}
					<div class="letter" class:exact class:close class:missing class:selected>
						{value}
						<span class="visually-hidden">
							{#if exact}(correct){:else if close}(present){:else if missing}(absent){:else}empty{/if}
						</span>
					</div>
				{/each}
			</div>
		{/each}
	</div>

	<div class="controls">
		{#if won || lost}
			{#if !won && answer}
				<p>the answer was "{answer}"</p>
			{/if}
			<button data-key="enter" class="restart selected" on:click={start_new_game}>
				{won ? 'you won :)' : `game over :(`} play again?
			</button>
		{:else}
			<div class="keyboard">
				<button data-key="enter" class:selected={submittable} disabled={!submittable} on:click={handle_enter}>enter</button>

				<button on:click|preventDefault={handle_keyboard_update} data-key="backspace">
					back
				</button>

				{#each ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'] as row}
					<div class="row">
						{#each row as letter}
							<button
								on:click|preventDefault={handle_keyboard_update}
								data-key={letter}
								class={classnames[letter]}
								disabled={guesses[i].length === 5 && !submittable}
								aria-label="{letter} {description[letter] || ''}"
							>
								{letter}
							</button>
						{/each}
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>

{#if won}
	<div
		style="position: absolute; left: 50%; top: 30%"
		use:confetti={{
			particleCount: $reduced_motion ? 0 : undefined,
			force: 0.7,
			stageWidth: window.innerWidth,
			stageHeight: window.innerHeight,
			colors: ['#ff3e00', '#40b3ff', '#676778']
		}}
	></div>
{/if}

<style>
	div {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		flex: 1;
	}

	.how-to-play {
		color: var(--color-text);
	}

	.how-to-play::before {
		content: 'i';
		display: inline-block;
		font-size: 0.8em;
		font-weight: 900;
		width: 1em;
		height: 1em;
		padding: 0.2em;
		line-height: 1;
		border: 1.5px solid var(--color-text);
		border-radius: 50%;
		text-align: center;
		margin: 0 0.5em 0 0;
		position: relative;
		top: -0.05em;
	}

	.grid {
		--width: min(100vw, 40vh, 380px);
		max-width: var(--width);
		align-self: center;
		justify-self: center;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
	}

	.grid .row {
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		grid-gap: 0.2rem;
		margin: 0 0 0.2rem 0;
	}

	@media (prefers-reduced-motion: no-preference) {
		.grid.bad-guess .row.current {
			animation: wiggle 0.5s;
		}
	}

	.grid.playing .row.current {
		filter: drop-shadow(3px 3px 10px var(--color-bg-0));
	}

	.letter {
		aspect-ratio: 1;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
		box-sizing: border-box;
		text-transform: lowercase;
		border: none;
		font-size: calc(0.08 * var(--width));
		border-radius: 2px;
		background: white;
		margin: 0;
		color: rgba(0, 0, 0, 0.7);
	}

	.letter.missing {
		background: rgba(255, 255, 255, 0.5);
		color: rgba(0, 0, 0, 0.5);
	}

	.letter.exact {
		background: var(--color-theme-2);
		color: white;
	}

	.letter.close {
		border: 2px solid var(--color-theme-2);
	}

	.selected {
		outline: 2px solid var(--color-theme-1);
	}

	.controls {
		text-align: center;
		justify-content: center;
		height: min(18vh, 10rem);
	}

	.keyboard {
		--gap: 0.2rem;
		position: relative;
		display: flex;
		flex-direction: column;
		gap: var(--gap);
		height: 100%;
	}

	.keyboard .row {
		display: flex;
		justify-content: center;
		gap: 0.2rem;
		flex: 1;
	}

	.keyboard button,
	.keyboard button:disabled {
		--size: min(8vw, 4vh, 40px);
		background-color: white;
		color: black;
		width: var(--size);
		border: none;
		border-radius: 2px;
		font-size: calc(var(--size) * 0.5);
		margin: 0;
	}

	.keyboard button.exact {
		background: var(--color-theme-2);
		color: white;
	}

	.keyboard button.missing {
		opacity: 0.5;
	}

	.keyboard button.close {
		border: 2px solid var(--color-theme-2);
	}

	.keyboard button:focus {
		background: var(--color-theme-1);
		color: white;
		outline: none;
	}

	.keyboard button[data-key='enter'],
	.keyboard button[data-key='backspace'] {
		position: absolute;
		bottom: 0;
		width: calc(1.5 * var(--size));
		height: calc(1 / 3 * (100% - 2 * var(--gap)));
		text-transform: uppercase;
		font-size: calc(0.3 * var(--size));
		padding-top: calc(0.15 * var(--size));
	}

	.keyboard button[data-key='enter'] {
		right: calc(50% + 3.5 * var(--size) + 0.8rem);
	}

	.keyboard button[data-key='backspace'] {
		left: calc(50% + 3.5 * var(--size) + 0.8rem);
	}

	.keyboard button[data-key='enter']:disabled {
		opacity: 0.5;
	}

	.restart {
		width: 100%;
		padding: 1rem;
		background: rgba(255, 255, 255, 0.5);
		border-radius: 2px;
		border: none;
	}

	.restart:focus,
	.restart:hover {
		background: var(--color-theme-1);
		color: white;
		outline: none;
	}

	@keyframes wiggle {
		0% {
			transform: translateX(0);
		}
		10% {
			transform: translateX(-2px);
		}
		30% {
			transform: translateX(4px);
		}
		50% {
			transform: translateX(-6px);
		}
		70% {
			transform: translateX(+4px);
		}
		90% {
			transform: translateX(-2px);
		}
		100% {
			transform: translateX(0);
		}
	}
</style>