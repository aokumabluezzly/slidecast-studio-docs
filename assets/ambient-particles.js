(() => {
  'use strict';

  if (document.querySelector('.ambient-particles')) return;

  const canvas = document.createElement('canvas');
  canvas.className = 'ambient-particles';
  canvas.setAttribute('aria-hidden', 'true');
  document.body.prepend(canvas);

  const context = canvas.getContext('2d');
  const motionQuery = matchMedia('(prefers-reduced-motion: reduce)');
  const colors = ['#3979e8', '#7657dc', '#d95d9f', '#67b8ff'];
  const pointer = { x: -9999, y: -9999, targetX: -9999, targetY: -9999, active: false };
  let width = 0;
  let height = 0;
  let ratio = 1;
  let seed = 1;
  let galaxies = [];
  let stars = [];
  let cursorTrail = [];
  let frame = 0;
  let previousTime = 0;
  let previousPointerTime = 0;

  function resetRandom() {
    seed = (0x51f15e + Math.round(width * 17) + Math.round(height * 29)) >>> 0;
  }

  function unitRandom() {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296;
  }

  const random = (min, max) => min + unitRandom() * (max - min);

  function galaxyLayout() {
    if (width < 680) {
      return [
        { x: 1.02, y: .16, radius: Math.max(260, width * .82), opacity: .72, tilt: -.34, flatten: .54, parallax: 22 },
        { x: -.08, y: .88, radius: Math.max(230, width * .7), opacity: .62, tilt: .46, flatten: .6, parallax: 16 }
      ];
    }

    const largeRadius = Math.max(430, Math.min(650, width * .42));
    return [
      { x: .82, y: .8, radius: largeRadius, opacity: .76, tilt: -.31, flatten: .54, parallax: 30 },
      { x: .04, y: .02, radius: largeRadius * .72, opacity: .48, tilt: .43, flatten: .59, parallax: 20 },
      { x: 1.02, y: .92, radius: largeRadius * .78, opacity: .55, tilt: -.72, flatten: .5, parallax: 24 }
    ];
  }

  function createGalaxy(config, galaxyIndex) {
    const armCount = galaxyIndex === 1 ? 3 : 4;
    const particleCount = Math.round(Math.min(1900, Math.max(900, config.radius * 3.6)));
    const particles = Array.from({ length: particleCount }, (_, particleIndex) => {
      const arm = particleIndex % armCount;
      const progress = Math.pow(unitRandom(), .78);
      const dust = unitRandom() < .16;
      const armOffset = (arm / armCount) * Math.PI * 2;
      const spiralTurns = galaxyIndex === 2 ? 1.45 : 1.82;
      const angle = armOffset + progress * spiralTurns * Math.PI * 2 + random(-.14, .14);
      const distance = progress * config.radius + random(-config.radius * .018, config.radius * .018);

      return {
        angle: dust ? random(0, Math.PI * 2) : angle,
        distance,
        dust,
        phase: random(0, Math.PI * 2),
        radius: random(.48, 1.45) * (1.12 - progress * .34),
        alpha: random(.22, .58) * (1.06 - progress * .38),
        color: colors[(arm + galaxyIndex + (particleIndex % 11 === 0 ? 3 : 0)) % colors.length]
      };
    });

    return {
      ...config,
      armCount,
      baseX: config.x * width,
      baseY: config.y * height,
      rotation: random(0, Math.PI * 2),
      rotationSpeed: random(.000012, .000026) * (galaxyIndex % 2 ? -1 : 1),
      driftPhase: random(0, Math.PI * 2),
      driftSpeed: random(.000055, .00009),
      driftX: random(18, 42),
      driftY: random(12, 30),
      particles
    };
  }

  function buildScene() {
    resetRandom();
    galaxies = galaxyLayout().map(createGalaxy);
    const starCount = width < 680 ? 85 : 180;
    stars = Array.from({ length: starCount }, (_, index) => ({
      x: random(0, width),
      y: random(0, height),
      radius: random(.35, 1),
      alpha: random(.08, .24),
      phase: random(0, Math.PI * 2),
      speed: random(.0015, .004) * (index % 2 ? -1 : 1),
      color: colors[index % colors.length]
    }));
  }

  function resize() {
    width = innerWidth;
    height = innerHeight;
    ratio = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    buildScene();
    render(performance.now(), true);
  }

  function drawStarfield(time, dark) {
    stars.forEach(star => {
      const x = (star.x + time * star.speed + width) % width;
      const twinkle = .72 + Math.sin(time * .0015 + star.phase) * .28;
      context.beginPath();
      context.arc(x, star.y, star.radius, 0, Math.PI * 2);
      context.globalAlpha = star.alpha * twinkle * (dark ? 1.35 : .88);
      context.fillStyle = star.color;
      context.fill();
    });
  }

  function drawGalaxy(galaxy, galaxyIndex, time, elapsed, dark, still) {
    if (!still) galaxy.rotation += galaxy.rotationSpeed * elapsed;

    const pointerX = pointer.active ? (pointer.x / width - .5) * galaxy.parallax : 0;
    const pointerY = pointer.active ? (pointer.y / height - .5) * galaxy.parallax : 0;
    const drift = time * galaxy.driftSpeed + galaxy.driftPhase;
    const centerX = galaxy.baseX + Math.cos(drift) * galaxy.driftX + pointerX;
    const centerY = galaxy.baseY + Math.sin(drift * .83) * galaxy.driftY + pointerY;

    const haloRadius = Math.min(150, galaxy.radius * .3);
    const halo = context.createRadialGradient(centerX, centerY, 0, centerX, centerY, haloRadius);
    halo.addColorStop(0, dark ? 'rgba(185,207,255,.42)' : 'rgba(102,151,255,.2)');
    halo.addColorStop(.16, dark ? 'rgba(118,87,220,.2)' : 'rgba(118,87,220,.09)');
    halo.addColorStop(.48, dark ? 'rgba(217,93,159,.08)' : 'rgba(217,93,159,.035)');
    halo.addColorStop(1, 'rgba(118,87,220,0)');
    context.beginPath();
    context.arc(centerX, centerY, haloRadius, 0, Math.PI * 2);
    context.globalAlpha = galaxy.opacity;
    context.fillStyle = halo;
    context.fill();

    const tiltCos = Math.cos(galaxy.tilt);
    const tiltSin = Math.sin(galaxy.tilt);

    context.save();
    context.lineWidth = dark ? 1.2 : .9;
    context.globalAlpha = galaxy.opacity * (dark ? .22 : .14);
    for (let arm = 0; arm < galaxy.armCount; arm += 1) {
      context.beginPath();
      for (let point = 0; point <= 150; point += 1) {
        const progress = point / 150;
        const angle = (arm / galaxy.armCount) * Math.PI * 2 + progress * 1.82 * Math.PI * 2 + galaxy.rotation;
        const distance = progress * galaxy.radius;
        const localX = Math.cos(angle) * distance;
        const localY = Math.sin(angle) * distance * galaxy.flatten;
        const x = centerX + localX * tiltCos - localY * tiltSin;
        const y = centerY + localX * tiltSin + localY * tiltCos;
        if (point === 0) context.moveTo(x, y);
        else context.lineTo(x, y);
      }
      context.strokeStyle = colors[(arm + galaxyIndex) % colors.length];
      context.stroke();
    }
    context.restore();

    galaxy.particles.forEach(particle => {
      const differentialSpin = particle.dust ? .14 : (particle.distance / galaxy.radius) * .045;
      const angle = particle.angle + galaxy.rotation + Math.sin(time * .00013 + particle.phase) * differentialSpin;
      const localX = Math.cos(angle) * particle.distance;
      const localY = Math.sin(angle) * particle.distance * galaxy.flatten;
      let x = centerX + localX * tiltCos - localY * tiltSin;
      let y = centerY + localX * tiltSin + localY * tiltCos;
      let reaction = 0;

      if (pointer.active) {
        const dx = x - pointer.x;
        const dy = y - pointer.y;
        const distance = Math.hypot(dx, dy) || 1;
        if (distance < 230) {
          reaction = Math.pow(1 - distance / 230, 2);
          const push = reaction * 46;
          x += (dx / distance) * push;
          y += (dy / distance) * push;
        }
      }

      const core = Math.max(0, 1 - particle.distance / (galaxy.radius * .18));
      const twinkle = .76 + Math.sin(time * .0018 + particle.phase) * .24;
      const radius = particle.radius * (1 + core * .65 + reaction * .6);
      context.beginPath();
      context.arc(x, y, radius, 0, Math.PI * 2);
      context.globalAlpha = Math.min(.84, particle.alpha * galaxy.opacity * twinkle * (dark ? 1.22 : 1) * (1 + core * .55 + reaction));
      context.fillStyle = particle.color;
      context.fill();
    });

    if (galaxyIndex === 0) {
      const core = context.createRadialGradient(centerX, centerY, 0, centerX, centerY, 34);
      core.addColorStop(0, dark ? 'rgba(245,248,255,.82)' : 'rgba(255,255,255,.9)');
      core.addColorStop(.22, dark ? 'rgba(130,174,255,.5)' : 'rgba(85,135,244,.3)');
      core.addColorStop(1, 'rgba(103,184,255,0)');
      context.beginPath();
      context.arc(centerX, centerY, 34, 0, Math.PI * 2);
      context.globalAlpha = galaxy.opacity;
      context.fillStyle = core;
      context.fill();
    }
  }

  function drawCursorTrail(elapsed, dark) {
    cursorTrail = cursorTrail.filter(particle => {
      particle.life -= elapsed * .00105;
      if (particle.life <= 0) return false;
      particle.x += particle.vx * elapsed;
      particle.y += particle.vy * elapsed;
      context.beginPath();
      context.arc(particle.x, particle.y, particle.radius * particle.life, 0, Math.PI * 2);
      context.globalAlpha = particle.life * (dark ? .72 : .58);
      context.fillStyle = particle.color;
      context.fill();
      return true;
    });
  }

  function render(time, still = false) {
    const elapsed = previousTime ? Math.min(time - previousTime, 34) : 16;
    previousTime = time;
    context.clearRect(0, 0, width, height);
    const dark = document.documentElement.dataset.theme === 'dark';

    if (pointer.active) {
      pointer.x += (pointer.targetX - pointer.x) * .14;
      pointer.y += (pointer.targetY - pointer.y) * .14;
    }

    drawStarfield(time, dark);
    galaxies.forEach((galaxy, index) => drawGalaxy(galaxy, index, time, elapsed, dark, still));
    drawCursorTrail(elapsed, dark);
    context.globalAlpha = 1;
    if (!motionQuery.matches && !still) frame = requestAnimationFrame(render);
  }

  function start() {
    cancelAnimationFrame(frame);
    previousTime = 0;
    if (motionQuery.matches) render(performance.now(), true);
    else frame = requestAnimationFrame(render);
  }

  addEventListener('resize', resize, { passive: true });
  addEventListener('pointermove', event => {
    if (motionQuery.matches || event.pointerType === 'touch') return;
    pointer.targetX = event.clientX;
    pointer.targetY = event.clientY;
    if (!pointer.active) {
      pointer.x = event.clientX;
      pointer.y = event.clientY;
      pointer.active = true;
    }

    const now = performance.now();
    if (now - previousPointerTime > 22) {
      previousPointerTime = now;
      for (let index = 0; index < 5; index += 1) {
        cursorTrail.push({
          x: event.clientX + random(-12, 12),
          y: event.clientY + random(-12, 12),
          vx: random(-.035, .035),
          vy: random(-.055, .018),
          radius: random(.8, 1.7),
          life: random(.65, 1),
          color: colors[Math.floor(random(0, colors.length))]
        });
      }
      if (cursorTrail.length > 110) cursorTrail.splice(0, cursorTrail.length - 110);
    }
  }, { passive: true });
  document.documentElement.addEventListener('pointerleave', () => {
    pointer.active = false;
  });
  motionQuery.addEventListener('change', start);
  new MutationObserver(() => render(performance.now(), true)).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cancelAnimationFrame(frame);
    else start();
  });

  resize();
  start();
})();
