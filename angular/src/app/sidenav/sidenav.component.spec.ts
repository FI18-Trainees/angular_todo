import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatSidenavModule, MatCheckboxModule, MatDividerModule } from '@angular/material';

import { SidenavComponent } from './sidenav.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Priority } from 'src/enums/priority.enum';
import { By } from '@angular/platform-browser';
import { Todo } from 'src/interfaces/todo';

describe('SidenavComponent', () => {
  let component: SidenavComponent;
  let fixture: ComponentFixture<SidenavComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatSidenavModule,
        BrowserAnimationsModule,
        MatCheckboxModule,
        MatDividerModule
      ],
      declarations: [ SidenavComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SidenavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('details should be displayed', () => {
    const now = new Date(Date.now());
    const testTodo: Todo = {
      title: 'testValue',
      id: 0,
      finished: false,
      priority: Priority.normal,
      list: 'testList',
      address: 'testAddress',
      description: 'testDescription',
      due_date: now,
      reminder: now,
      subtask: ['testSubtask1', 'testSubtask2']
    };
    component.displayedTodo = testTodo;
    fixture.detectChanges();
    expect(fixture.debugElement.query(By.css('.header')).nativeElement.innerHTML).toContain(testTodo.title);
    expect(fixture.debugElement.query(By.css('.details')).nativeElement.innerHTML).toContain(testTodo.due_date.toLocaleDateString());
    expect(fixture.debugElement.query(By.css('.details')).nativeElement.innerHTML).toContain(testTodo.reminder.toLocaleDateString());
    expect(fixture.debugElement.query(By.css('.details')).nativeElement.innerHTML).toContain(testTodo.priority);
    expect(fixture.debugElement.query(By.css('.details')).nativeElement.innerHTML).toContain(testTodo.address);
    expect(fixture.debugElement.query(By.css('.details')).nativeElement.innerHTML).toContain(testTodo.description);
  });
});
