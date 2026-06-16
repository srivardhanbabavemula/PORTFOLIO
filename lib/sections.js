import profile from '@/data/profile.json'

export const PROJECT_COUNT = profile.projects.length

/** Viewport snap indices — must stay in sync with section order in page.js */
export const SECTION = {
  VIDEO: 0,
  HERO: 1,
  ABOUT: 2,
  PROJECTS: 3,
  get EXPERIENCE() { return this.PROJECTS + PROJECT_COUNT },
  get SKILLS() { return this.EXPERIENCE + 1 },
  get CERTIFICATIONS() { return this.SKILLS + 1 },
  get PUBLICATIONS() { return this.CERTIFICATIONS + 1 },
  get CONTACT() { return this.PUBLICATIONS + 2 },
}

/** Total wheel-snap positions (projects + 2 new sections + work + 3-step footer) */
export const TOTAL_SNAPS = 9 + PROJECT_COUNT

export const NAV_ITEMS = [
  { label: 'Home',         idx: SECTION.VIDEO },
  { label: 'About',        idx: SECTION.ABOUT },
  { label: 'Work',         idx: SECTION.PROJECTS },
  { label: 'Experience',   idx: SECTION.EXPERIENCE },
  { label: 'Skills',       idx: SECTION.SKILLS },
  { label: 'Certs',        idx: SECTION.CERTIFICATIONS },
  { label: 'Contact',      idx: SECTION.CONTACT },
]

export function scrollToSection(idx) {
  if (typeof window === 'undefined') return
  window.dispatchEvent(new CustomEvent('navigate-section', { detail: { idx } }))
}
