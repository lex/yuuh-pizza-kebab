begin;

-- Demo user
insert into YPKUser (username, password) values ('yuuh', 'yuuh');

-- Demo kebabs
insert into Kebab (name, price) values ('Kebab with french fries', 9.00);
insert into Kebab (name, price) values ('Kebab with rice', 8.30);
insert into Kebab (name, price) values ('Iskender kebab', 8.90);
insert into Kebab (name, price) values ('Pita kebab', 8.50);

-- Demo toppings
insert into Topping (name, price) values ('Ground beef', 1.00);
insert into Topping (name, price) values ('Shrimp', 1.00);
insert into Topping (name, price) values ('Clams', 1.00);
insert into Topping (name, price) values ('Tuna', 1.00);
insert into Topping (name, price) values ('Pineapple', 1.00);
insert into Topping (name, price) values ('Exotic cheese', 1.00);
insert into Topping (name, price) values ('Salami', 1.00);

-- Demo pizzas
insert into Pizza (name, price) values ('Bolognese', 7.20);
insert into Pizza (name, price) values ('Frutti di Mare', 8.10);
insert into Pizza (name, price) values ('Romeo', 8.20);

-- Link toppings to the pizzas
insert into Pizza_Topping (pizza_id, topping_id) values ((select id from Pizza where name like 'Bolognese'), (select id from Topping where name like 'Ground beef'));

insert into Pizza_Topping (pizza_id, topping_id) values ((select id from Pizza where name like 'Frutti di Mare'), (select id from Topping where name like 'Shrimp'));
insert into Pizza_Topping (pizza_id, topping_id) values ((select id from Pizza where name like 'Frutti di Mare'), (select id from Topping where name like 'Clams'));
insert into Pizza_Topping (pizza_id, topping_id) values ((select id from Pizza where name like 'Frutti di Mare'), (select id from Topping where name like 'Tuna'));

insert into Pizza_Topping (pizza_id, topping_id) values ((select id from Pizza where name like 'Romeo'), (select id from Topping where name like 'Shrimp'));
insert into Pizza_Topping (pizza_id, topping_id) values ((select id from Pizza where name like 'Romeo'), (select id from Topping where name like 'Pineapple'));
insert into Pizza_Topping (pizza_id, topping_id) values ((select id from Pizza where name like 'Romeo'), (select id from Topping where name like 'Exotic cheese'));
insert into Pizza_Topping (pizza_id, topping_id) values ((select id from Pizza where name like 'Romeo'), (select id from Topping where name like 'Salami'));

-- Add some drinks as well

insert into Drink (name, price) values ('Cola', 0.49);
insert into Drink (name, price) values ('Orange juice', 0.49);
insert into Drink (name, price) values ('Milk', 0.39);
insert into Drink (name, price) values ('Beer', 0.99);
insert into Drink (name, price) values ('Imported beer', 1.99);

commit;
