import profile from '@/data/profile.json'

export const PROJECT_COUNT = profile.projects.length

/** Viewport snap indices — must stay in sync with section order in page.js */
export const SECTION = {
  VIDEO: 0,
  HERO: 1,
  ABOUT: 2,
  EXPERIENCE: 3,
  PROJECTS: 4,
  get SKILLS() { return this.PROJECTS + PROJECT_COUNT },
  get CERTIFICATIONS() { return this.SKILLS + 1 },
  get PUBLICATIONS() { return this.CERTIFICATIONS + 1 },
  get CONTACT() { return this.PUBLICATIONS + 2 },
}

/** Total wheel-snap positions */
export const TOTAL_SNAPS = 9 + PROJECT_COUNT

export const NAV_ITEMS = [
  { label: 'Home',         idx: SECTION.VIDEO },
  { label: 'About',        idx: SECTION.ABOUT },
  { label: 'Experience',   idx: SECTION.EXPERIENCE },
  { label: 'Projects',     idx: SECTION.PROJECTS },
  { label: 'Skills',       idx: SECTION.SKILLS },
  { label: 'Certs',        idx: SECTION.CERTIFICATIONS },
  { label: 'Contact',      idx: SECTION.CONTACT },
]

export function scrollToSection(idx) {
  if (typeof window === 'undefined') return
  window.dispatchEvent(new CustomEvent('navigate-section', { detail: { idx } }))
}
