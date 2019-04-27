

fn main() {
    let x = 10;
    for i in 0..x {
        let m = if i % 2 == 0 {"even"} else {"odd"};
        println!("{} {}", m, i);
    }
}


