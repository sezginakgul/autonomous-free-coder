import {useState} from "react"
import {menu} from "./data/menu"
import Sidebar from "./components/Sidebar"
import ProductGrid from "./components/ProductGrid"
import Cart from "./components/Cart"

export default function App(){

const [selected,setSelected]=useState("Tümü")
const [cart,setCart]=useState([])

const filtered = selected==="Tümü"
? menu
: menu.filter(m=>m.category===selected)

const add = (p)=>{

const exist = cart.find(i=>i.id===p.id)

if(exist){

setCart(cart.map(i=>
i.id===p.id
? {...i,qty:i.qty+1}
: i
))

}else{

setCart([...cart,{...p,qty:1}])

}

}

const inc = (id)=>{
setCart(cart.map(i=>i.id===id?{...i,qty:i.qty+1}:i))
}

const dec = (id)=>{
setCart(cart
.map(i=>i.id===id?{...i,qty:i.qty-1}:i)
.filter(i=>i.qty>0))
}

return(

<div className="grid grid-cols-[200px_1fr_320px] h-screen">

<Sidebar selected={selected} setSelected={setSelected}/>

<ProductGrid products={filtered} add={add}/>

<Cart cart={cart} inc={inc} dec={dec}/>

</div>

)

}