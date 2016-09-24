begin;

-- Demo user
insert into YPKUser (username, password, is_admin) values ('yuuh', 'yuuh', true);

-- Demo kebabs
insert into Kebab (name, price, image_url) values ('Kebab with french fries', 9.00, '/static/img/demo/kebabfrenchfries.jpg');
insert into Kebab (name, price, image_url) values ('Kebab with rice', 8.30, '/static/img/demo/ricekebab.jpg');
insert into Kebab (name, price, image_url) values ('Iskender kebab', 8.90, '/static/img/demo/iskenderkebab.jpg');
insert into Kebab (name, price, image_url) values ('Pita kebab', 8.50, '/static/img/demo/pitakebab.jpg');

-- Demo toppings
insert into Topping (name, price) values ('Ground beef', 1.00);
insert into Topping (name, price) values ('Shrimp', 1.00);
insert into Topping (name, price) values ('Clams', 1.00);
insert into Topping (name, price) values ('Tuna', 1.00);
insert into Topping (name, price) values ('Pineapple', 1.00);
insert into Topping (name, price) values ('Exotic cheese', 1.00);
insert into Topping (name, price) values ('Salami', 1.00);

-- Demo pizzas
insert into Pizza (name, price, image_url) values ('Bolognese', 7.20, '/static/img/demo/bolognese.jpg');
insert into Pizza (name, price, image_url) values ('Frutti di Mare', 8.10, '/static/img/demo/fruttidimare.jpg');
insert into Pizza (name, price, image_url) values ('Romeo', 8.20, '/static/img/demo/romeo.jpg');

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

insert into Drink (name, price, image_url) values ('Cola', 0.49, '/static/img/demo/cola.jpg');
insert into Drink (name, price, image_url) values ('Orange juice', 0.49, '/static/img/demo/orangejuice.jpg');
insert into Drink (name, price, image_url) values ('Milk', 0.39, '/static/img/demo/milk.jpg');
insert into Drink (name, price, image_url) values ('Beer', 0.99, '/static/img/demo/beer.jpg');
insert into Drink (name, price, image_url) values ('Imported beer', 1.99, '/static/img/demo/importedbeer.jpg');

commit;
