<script>
	import { page } from '$app/stores';
	import Header from './Header.svelte';
	import './../app.css';
	import Toast from '$lib/components/Toast.svelte';

	let { children } = $props();

	// Check if we're on a 3D app route
	$effect(() => {
		const isAppRoute = $page.url.pathname.startsWith('/app');
		if (typeof window !== 'undefined') {
			if (isAppRoute) {
				document.documentElement.style.overflow = 'hidden';
				document.body.style.overflow = 'hidden';
				document.body.style.margin = '0';
				document.body.style.padding = '0';
			} else {
				document.documentElement.style.overflow = '';
				document.body.style.overflow = '';
				document.body.style.margin = '';
				document.body.style.padding = '';
			}
		}
	});
</script>

<div class="app" class:is-app-route={$page.url.pathname.startsWith('/app')}>
	<Toast />
	{#if !$page.url.pathname.startsWith('/app')}
		<Header />
	{/if}

	<main class:full-screen={$page.url.pathname.startsWith('/app')}>
		{#key $page.url.pathname}
			{@render children()}
		{/key}
	</main>

	{#if !$page.url.pathname.startsWith('/app')}
		<footer>
			<p>© 2023 - PRESENT</p>
		</footer>
	{/if}
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	.app.is-app-route {
		min-height: 100vh;
		height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	main.full-screen {
		padding: 0;
		max-width: 100%;
		width: 100%;
		height: 100vh;
		margin: 0;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>