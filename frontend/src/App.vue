<script setup>
import { AlbumCovers, Home, List, Search, User } from '@boxicons/vue';
</script>

<template>
    <header>
        <nav>
            <router-link to="/" class="no-deco">
                <h2 class="name">Chore Tracker</h2>
            </router-link>

            <div class="flex-row align-center">
                <ul>
                    <li>
                        <router-link 
                            class="btn btn-text no-deco" 
                            to="/transactions"
                        >
                            <List pack="filled" size="sm"/>
                            <span>Transactions</span>
                        </router-link>
                    </li>
                    <li>
                        <router-link 
                            class="btn btn-text no-deco" 
                            to="/analytics"
                        >
                            <AlbumCovers pack="filled" size="sm"/>
                            <span>Analytics</span>
                        </router-link>
                    </li>
                </ul>
                <router-link 
                    class="btn btn-user btn-even-padding no-deco"
                    to="/account"
                >
                    <User pack="filled" size="sm"/>
                </router-link>
            </div>
        </nav>

        <div class="background"></div>
    </header>

    <nav class="mobile-nav" :class="{'nav-visible': displayNav}">
        <router-link class="btn btn-text no-deco" to="/">
            <Home pack="filled"/>
            <span>Home</span>
        </router-link>
        <router-link class="btn btn-text no-deco" to="/transactions">
            <List pack="filled"/>
            <span>Transactions</span>
        </router-link>
        <router-link class="btn btn-text no-deco" to="/new">
            <Search pack="basic"/>
            <span>New</span>
        </router-link>
        <router-link class="btn btn-text no-deco" to="/analytics">
            <AlbumCovers pack="filled"/>
            <span>Analytics</span>
        </router-link>
        <router-link class="btn btn-text no-deco" to="/account">
            <User pack="filled"/>
            <span>Account</span>
        </router-link>
    </nav>

    <main :class="{'nav-visible': displayNav}">
        <router-view :key="$route.path"/>
    </main>

    <footer :class="{'nav-visible': displayNav}">
        © Aleksi Malkki 2026. All Rights Reserved.
    </footer>
</template>

<style scoped>
header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    padding: var(--spacing-sm-md) var(--spacing-md);
    border-bottom: 1px solid var(--c-border);
    z-index: var(--z-nav);

    nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .background {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        backdrop-filter: blur(var(--blur-heavy));
        background: var(--c-bg-opaque-base);
    }
}

nav.mobile-nav {
    display: none;
}

.name {
    margin: 0;
    color: var(--c-text);
}

.search-bar {
    margin-left: var(--spacing-lg);
    margin-right: var(--spacing-md);
}

ul {
    list-style-type: none;
    display: flex;
    padding: 0;
    margin: 0;
    /* gap: var(--spacing-sm); */
}

header .btn {
    padding: var(--spacing-sm) var(--spacing-sm-md);
    font-size: var(--fs-0);
    display: flex;
    align-items: center;
}

.btn.btn-user {
    margin-left: var(--spacing-sm);
    border-radius: 100px;
    aspect-ratio: 1;
    padding: var(--spacing-sm);
}

main {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}
main.nav-visible {
    margin-top: 64px;
}

footer {
    margin-top: auto;
    margin-bottom: 0;
    justify-content: center;
    display: flex;
    padding: var(--spacing-sm) 0;
}

footer a {
    color: var(--c-text-subtle);
}


@media(max-width: 768px) {
    header {
        display: none;
    }

    main.nav-visible {
        margin-top: 0;
        margin-bottom: 64px;
    }

    footer {
        display: none;
    }

    nav.mobile-nav.nav-visible {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;

        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: var(--spacing-sm) var(--spacing-md);
        border-top: 1px solid var(--c-border);
        backdrop-filter: blur(var(--blur-heavy));
        background: var(--c-bg-opaque-base);

        z-index: var(--z-nav);

        .btn {
            flex: 1;
            padding-inline: 0;
            /* border-radius: 100px; */
            flex-direction: column;

            span {
                font-size: var(--fs-neg-4);
                font-weight: 500;
                opacity: 0.5;
            }
        }
    }
}

</style>
