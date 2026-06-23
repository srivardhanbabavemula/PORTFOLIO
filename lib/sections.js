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
  { label: 'Home',             idx: SECTION.VIDEO,           featured: false },
  { label: 'About',            idx: SECTION.ABOUT,           featured: false },
  { label: 'Education',        idx: SECTION.EDUCATION,       featured: true  },
  { label: 'Experience',       idx: SECTION.EXPERIENCE,      featured: false },
  { label: 'Accomplishments',  idx: SECTION.ACCOMPLISHMENTS, featured: true  },
  { label: 'Projects',         idx: SECTION.PROJECTS,        featured: false },
  { label: 'Skills',           idx: SECTION.SKILLS,          featured: false },
  { label: 'Certs',            idx: SECTION.CERTIFICATIONS,  featured: false },
  { label: 'Contact',          idx: SECTION.CONTACT,         featured: false },
]

export function scrollToSection(idx) {
  if (typeof window === 'undefined') return
  window.dispatchEvent(new CustomEvent('navigate-section', { detail: { idx } }))
}
