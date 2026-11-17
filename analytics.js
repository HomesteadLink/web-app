/* PostHog analytics for the HomeSteadyLink web app (USB setup)
 * (growth-analytics lane).
 *
 * Loads the official PostHog JS snippet and inits it with the key from
 * posthog-config.js. Until a key is set, window.hslAnalytics is a
 * no-op stub, so every capture() call in index.html is safe.
 *
 * What is tracked (autocapture, on by default): $pageview and
 * $autocapture (clicks). Explicit events from index.html:
 * - `webapp_connected` — router connected over USB, Wi-Fi scan done.
 * - `webapp_provision_started` — Wi-Fi (+VPN) submitted, progress began.
 * - `onboarding_done` + `core_action_done` — first time per browser
 *   the router reaches ONLINE (the web setup completing); later times
 *   send `core_action_repeat` instead (localStorage flag).
 * No personal data is ever captured: no SSID, no Wi-Fi password, no
 * Tailscale auth key, no WireGuard config, no device serial, no email.
 * Person profiles are 'identified_only' (anonymous by default — the
 * app has no login, so identify is never called).
 */
(function () {
  var key = window.HSL_POSTHOG_API_KEY || "";
  var host = window.HSL_POSTHOG_HOST || "https://us.i.posthog.com";

  // No key yet: stub so callers never throw.
  if (!key) {
    window.hslAnalytics = {
      enabled: false,
      capture: function () {},
      coreActionDone: function () {},
    };
    return;
  }

  // Official PostHog JS snippet (posthog.com/docs/libraries/js).
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],Object.defineProperty(u,"toString",{configurable:!0,enumerable:!0,writable:!0,value:function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}}),Object.defineProperty(u.people,"toString",{configurable:!0,enumerable:!0,writable:!0,value:function(){return u.toString(1)+".people (stub)"}}),o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagResult isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  posthog.init(key, {
    api_host: host,
    defaults: "2026-08-30",
    person_profiles: "identified_only",
  });

  window.hslAnalytics = {
    enabled: true,
    capture: function (event, props) {
      posthog.capture(event, props || {});
    },
    // First online per browser: onboarding_done + core_action_done;
    // later times: core_action_repeat. Mirrors the Android funnel.
    coreActionDone: function (props) {
      var done = false;
      try { done = localStorage.getItem("hsl_onboarding_done") === "1"; } catch (e) {}
      if (!done) {
        try { localStorage.setItem("hsl_onboarding_done", "1"); } catch (e) {}
        posthog.capture("onboarding_done", props || {});
        posthog.capture("core_action_done", props || {});
      } else {
        posthog.capture("core_action_repeat", props || {});
      }
    },
  };
})();
