import { Component, OnInit } from '@angular/core';
import { TodoService } from 'src/services/todo.service';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.scss']
})
export class InputComponent implements OnInit {

  inputValue: string;
  selectedDate: Date;

  constructor(private todoService: TodoService) { }

  ngOnInit() {
  }

  handleInput(e: KeyboardEvent) {
    e.preventDefault();
    if (this.selectedDate) {
      this.todoService.addTodo(this.inputValue, this.selectedDate);
    } else {
      this.todoService.addTodo(this.inputValue);
    }
    this.inputValue = '';
    this.selectedDate = null;
  }
}
