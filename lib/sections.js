import profile from '@/data/profile.json'

export const PROJECT_COUNT = profile.projects.length

/** Viewport snap indices — must stay in sync with section order in page.js */
export const SECTION = {
  VIDEO: 0,
  HERO: 1,
  ABOUT: 2,
  EDUCATION: 3,
  EXPERIENCE: 4,
  ACCOMPLISHMENTS: 5,
  PROJECTS: 6,
  get SKILLS() { return this.PROJECTS + PROJECT_COUNT },
  get CERTIFICATIONS() { return this.SKILLS + 1 },
  get PUBLICATIONS() { return this.CERTIFICATIONS + 1 },
  get CONTACT() { return this.PUBLICATIONS + 2 },
}

/** Total wheel-snap positions */
export const TOTAL_SNAPS = 11 + PROJECT_COUNT

export const NAV_ITEMS = [
  { label: 'Home',            idx: SECTION.VIDEO },
  { label: 'About',           idx: SECTION.ABOUT },
  { label: 'Education',       idx: SECTION.EDUCATION },
  { label: 'Experience',      idx: SECTION.EXPERIENCE },
  { label: 'Accomplishments', idx: SECTION.ACCOMPLISHMENTS },
  { label: 'Projects',        idx: SECTION.PROJECTS },
  { label: 'Skills',          idx: SECTION.SKILLS },
  { label: 'Certs',           idx: SECTION.CERTIFICATIONS },
  { label: 'Contact',         idx: SECTION.CONTACT },
]

export function isNavItemActive(label, idx, activeIdx) {
  switch (label) {
    case 'Home':
      return activeIdx <= SECTION.HERO
    case 'Projects':
      return activeIdx >= SECTION.PROJECTS && activeIdx < SECTION.SKILLS
    case 'Contact':
      return activeIdx >= SECTION.PUBLICATIONS
    default:
      return activeIdx === idx
  }
}

export function scrollToSection(idx) {
  if (typeof window === 'undefined') return
  window.dispatchEvent(new CustomEvent('navigate-section', { detail: { idx } }))
}
