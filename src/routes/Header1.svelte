<script>
	// import App from './../lib/components/App.svelte';
	import { page } from '$app/stores';
	import logo from '$lib/images/svelte-logo.svg'; 
	import github from '$lib/images/github.svg'; 
</script>

<header>
	<div class="corner">
		<a href="https://kit.svelte.dev">
			<img src={logo} alt="SvelteKit" />
		</a>
	</div>

	<nav>
		<svg viewBox="0 0 2 3" aria-hidden="true">
			<path d="M0,0 L1,2 C1.5,3 1.5,3 2,3 L2,0 Z" />
		</svg>
		<ul>
			<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
				<a href="/">Home</a>
			</li>
			<li aria-current={$page.url.pathname === '/about' ? 'page' : undefined}>
				<a href="/about">About</a>
			</li>
			<li aria-current={$page.url.pathname.startsWith('/sverdle') ? 'page' : undefined}>
				<a href="/sverdle">Sverdle</a>
			</li>
			<li aria-current={$page.url.pathname === '/vague' ? 'page' : undefined}>
				<a href="/vague">Vague</a>
			</li>

			<li aria-current={$page.url.pathname === '/models' ? 'page' : undefined}>
				<a href="/models">model</a>
			</li>
			<li aria-current={$page.url.pathname === '/sphere2' ? 'page' : undefined}>
				<a href="/sphere">sphere</a>
			</li>
			<li aria-current={$page.url.pathname === '/Spaceship' ? 'page' : undefined}>
				<a href="/Spaceship">Spaceship</a>
			</li>
			<li aria-current={$page.url.pathname === '/desksc' ? 'page' : undefined}>
				<a href="/desksc">desktop</a>
			</li>
			<li aria-current={$page.url.pathname === '/films' ? 'page' : undefined}>
				<a href="/films">films</a>
			</li>
			<li aria-current={$page.url.pathname === '/app/' ? 'page' : undefined}> 
				<a href="/app/">App</a> 
			</li> 
			<li aria-current={$page.url.pathname === '/mdwd/' ? 'page' : undefined}>
				<a href="/mdwd/">mdwd</a>
			</li> 
			<li aria-current={$page.url.pathname === '/bibi/' ? 'page' : undefined}>
				<a href="/bibi/">Bibi</a>
			</li>
			<li aria-current={$page.url.pathname === '/planet/' ? 'page' : undefined}>
				<a href="/planet/">Planet</a>
			</li>
			<li aria-current={$page.url.pathname === '/fkisios-main/' ? 'page' : undefined}>
				<a href="/fkisios-main/">GameZ</a>
			</li>
		</ul>

		<svg viewBox="0 0 2 3" aria-hidden="true">
			<path d="M0,0 L0,3 C0.5,3 0.5,3 1,2 L2,0 Z" />
		</svg>
	</nav>

	<div class="corner">
		<a href="https://github.com/sveltejs/kit">
			<img src={github} alt="GitHub" />
		</a>
	</div>
</header>

<style>
	header {
		display: flex;
		justify-content: space-between;
	}

	.corner {
		width: 3em;
		height: 3em;
	}

	.corner a {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.corner img {
		width: 2em;
		height: 2em;
		object-fit: contain;
	}

	nav {
		display: flex;
		justify-content: center;
		--background: rgba(255, 255, 255, 0.3);
	}

	svg {
		width: 2em;
		height: 3em;
		display: block;
	}

	path {
		fill: var(--background);
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);

	}

	li {
		position: relative;
		height: 100%;
		background: transparent; /* transparent */
		z-index: 10;
	}

	li[aria-current='page']::before {
		--size: 6px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-theme-1);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: var(--color-text);
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-theme-1);
	}
</style>
