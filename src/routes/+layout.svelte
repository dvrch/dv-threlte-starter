<script>
	import { page } from '$app/stores';
	import Header from './Header.svelte';
	import './../app.css';
	import Toast from '$lib/components/Toast.svelte';

	let { children } = $props();

	// Check if we're on a wide route (3D apps)
	$effect(() => {
		const isWideRoute = $page.url.pathname.startsWith('/app') || $page.url.pathname.startsWith('/vague');
		if (typeof window !== 'undefined') {
			if (isWideRoute) {
				// We don't need to hijack body overflow anymore if we want standard scrolling/layout behavior
				// but for 3D scenes, disabling scroll on body is often good. 
				// The user wants "rester a coté des autres" (standard nav), so maybe keep scroll?
				// But "occuper presque tout" implies a fixed viewport.
				// Let's reset styles to default to be safe and let CSS handle layout.
				document.documentElement.style.overflow = '';
				document.body.style.overflow = '';
				document.body.style.margin = '';
				document.body.style.padding = '';
			} else {
				document.documentElement.style.overflow = '';
				document.body.style.overflow = '';
				document.body.style.margin = '';
				document.body.style.padding = '';
			}
		}
	});
</script>

<div class="app" class:is-app-route={$page.url.pathname.startsWith('/app') || $page.url.pathname.startsWith('/vague')}>
	<Toast />
	<Header />

	<main class:full-screen={$page.url.pathname.startsWith('/app') || $page.url.pathname.startsWith('/vague')}>
		{#key $page.url.pathname}
			{@render children()}
		{/key}
	</main>

	{#if !$page.url.pathname.startsWith('/app') && !$page.url.pathname.startsWith('/vague')}
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
		height: 100vh; /* Fixed height for 3D apps to prevent window compilation */
        overflow: hidden;
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
		/* height: 100vh; Removed to respect header */
        height: 100%; /* Fill flex parent */
		margin: 0;
        overflow: hidden; /* Prevent canvas scroll */
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