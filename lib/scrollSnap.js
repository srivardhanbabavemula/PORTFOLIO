import { SECTION, TOTAL_SNAPS } from '@/lib/sections'

function vh() {
  if (typeof window === 'undefined') return 800
  return window.innerHeight
}

/** Scroll position for a snap index — uses DOM offsets when available */
export function getScrollTopForIdx(idx, height = vh()) {
  if (typeof document === 'undefined') return idx * height

  const projects = document.querySelector('[data-snap-anchor="projects"]')
  const skills = document.querySelector('[data-snap-anchor="skills"]')
  const certifications = document.querySelector('[data-snap-anchor="certifications"]')
  const footer = document.querySelector('[data-snap-anchor="footer"]')
  const single = document.querySelector(`[data-snap-index="${idx}"]`)

  if (idx <= SECTION.ACCOMPLISHMENTS && single) {
    return single.offsetTop
  }

  if (idx >= SECTION.PROJECTS && idx < SECTION.SKILLS && projects) {
    return projects.offsetTop + (idx - SECTION.PROJECTS) * height
  }

  if (idx === SECTION.SKILLS && skills) return skills.offsetTop
  if (idx === SECTION.CERTIFICATIONS && certifications) return certifications.offsetTop

  if (idx >= SECTION.PUBLICATIONS && footer) {
    return footer.offsetTop + (idx - SECTION.PUBLICATIONS) * height
  }

  return idx * height
}

/** Nearest snap index for a scroll position */
export function getIdxFromScrollTop(scrollTop, height = vh()) {
  let bestIdx = 0
  let bestDist = Infinity

  for (let i = 0; i < TOTAL_SNAPS; i++) {
    const dist = Math.abs(scrollTop - getScrollTopForIdx(i, height))
    if (dist < bestDist) {
      bestDist = dist
      bestIdx = i
    }
  }

  return bestIdx
}

/** Nav highlight index — keeps Projects active inside the projects scroll range */
export function getNavActiveIdx(scrollTop, sectionIdx, height = vh()) {
  if (typeof document === 'undefined') return sectionIdx

  const projects = document.querySelector('[data-snap-anchor="projects"]')
  if (projects && scrollTop >= projects.offsetTop - height * 0.2) {
    const skills = document.querySelector('[data-snap-anchor="skills"]')
    const skillsTop = skills?.offsetTop ?? Infinity
    if (scrollTop < skillsTop - height * 0.35) {
      return Math.max(sectionIdx, SECTION.PROJECTS)
    }
  }

  return sectionIdx
}

export { vh as getViewportHeight }
