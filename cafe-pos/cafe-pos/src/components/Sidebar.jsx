const categories = ["Tümü","Kahveler","Tatlılar","Soğuk İçecekler"]

export default function Sidebar({selected,setSelected}){

return(

<div className="bg-white shadow-md p-4 flex flex-col gap-3">

{categories.map(cat=>(
<button
key={cat}
onClick={()=>setSelected(cat)}
className={`p-3 rounded-xl text-left ${
selected===cat
? "bg-slate-900 text-white"
: "bg-slate-100 hover:bg-slate-200"
}`}>
{cat}
</button>

))}

</div>

)

}