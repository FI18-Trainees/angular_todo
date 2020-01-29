import { Component, OnInit } from '@angular/core';
import { TodoService } from 'src/services/todo.service';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.scss']
})
export class InputComponent implements OnInit {

  inputValue;

  constructor(private todoService: TodoService) { }

  ngOnInit() {
  }

  handleInput(e: KeyboardEvent) {
    e.preventDefault();
    this.todoService.addTodo(this.inputValue);
    this.inputValue = '';
  }
}
