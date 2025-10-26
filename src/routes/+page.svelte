<script>
	export let data;
	export let params = {};
	import Counter from './Counter.svelte';
	import Spaceship from './Spaceship/+page.svelte';
	import Vague from './vague/+page.svelte';
	import Sphere from './sphere/+page.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
    import App from './sphere/+page.svelte';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section > 

	<h1>
		<span class="welcome">
			<picture>
				<source srcset={welcome} type="image/webp" />
				<img src={welcome_fallback} alt="Welcome" />
			</picture>
		</span>
		
		to DJONTSO<br />Svelte MULTI-App
	</h1>
	
	<h2>
		try editing <strong>src/routes/+page.svelte</strong>
	</h2>
	
</section>

<div class="div">
	<Spaceship />
</div>
<div class="div2">
	<!-- <Vague /> -->
	<App />
</div>


<Counter />

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
		color: blue;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
	
	.div {position: absolute; 
		top: 0; 
		left: 0; 
		width: 100%; 
		height: 100%; 
		z-index: -1;
	}

	.div2 {position: absolute; 
		top: 0; 
		left: 0; 
		width: 100%; 
		height: 100%; 
		z-index: -2;
		background: rgba(255, 255, 255, 0.5);
	}


</style>