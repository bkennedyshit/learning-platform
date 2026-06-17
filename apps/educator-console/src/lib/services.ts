export type Role = 'educator' | 'org_admin' | 'student';

export interface User {
  id: string;
  name: string;
  role: Role;
}

export interface Classroom {
  id: string;
  name: string;
  educatorIds: string[];
  studentIds: string[];
  assignedPathId: string | null;
}

export interface Organization {
  id: string;
  name: string;
  purchasedSeats: number;
  usedSeats: number;
}

export interface StudentProgress {
  studentId: string;
  completedLessons: number;
  lastActivity: string;
  needsReview: boolean;
  graspScore: number;
}

// Mocks
let org: Organization = {
  id: 'org1',
  name: 'Springfield High',
  purchasedSeats: 50,
  usedSeats: 48,
};

let classrooms: Classroom[] = [
  {
    id: 'class1',
    name: 'Algebra 101',
    educatorIds: ['edu1'],
    studentIds: ['stu1', 'stu2'],
    assignedPathId: 'path_algebra',
  }
];

let progress: Record<string, StudentProgress> = {
  stu1: { studentId: 'stu1', completedLessons: 12, lastActivity: new Date().toISOString(), needsReview: true, graspScore: 65 },
  stu2: { studentId: 'stu2', completedLessons: 15, lastActivity: new Date().toISOString(), needsReview: false, graspScore: 85 },
};

export const orgService = {
  getOrganization: async () => org,
  getClassrooms: async () => classrooms,
  createClassroom: async (name: string, educatorId: string) => {
    const newClass = { id: `class${Date.now()}`, name, educatorIds: [educatorId], studentIds: [], assignedPathId: null };
    classrooms.push(newClass);
    return newClass;
  },
  addStudentToClassroom: async (classroomId: string, studentId: string) => {
    if (org.usedSeats >= org.purchasedSeats) {
      throw new Error('Seat limit reached: Cannot add student beyond purchased seats.');
    }
    const c = classrooms.find(c => c.id === classroomId);
    if (c) {
      c.studentIds.push(studentId);
      org.usedSeats++;
    }
  },
  assignPath: async (classroomId: string, pathId: string) => {
    const c = classrooms.find(c => c.id === classroomId);
    if (c) c.assignedPathId = pathId;
  }
};

export const progressService = {
  getStudentProgress: async (studentIds: string[]) => {
    return studentIds.map(id => progress[id] || {
      studentId: id, completedLessons: 0, lastActivity: new Date().toISOString(), needsReview: false, graspScore: 0
    });
  }
};
