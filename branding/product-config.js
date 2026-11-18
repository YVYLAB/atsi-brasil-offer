/* Registro visual compartilhado. Nunca definir catálogo ou preços por empresa aqui. */
(function(root){
  'use strict';
  const companies=Object.freeze({
    'atsi-brasil':{
      slug:'atsi-plus',client:'ATSI Brasil',shortName:'ATSI',
      logoInstitutional:'branding/assets/atsi-logo-cabecalho.svg',
      logoDark:'logo-dark.svg',logoLight:'logo-light.svg',favicon:'icon.svg'
    },
    jan:{
      slug:'jan',client:'JAN',shortName:'JAN',
      logoInstitutional:'assets/companies/jan/logo-institucional.svg',
      logoDark:'logo-institucional.svg',logoLight:'logo-institucional.svg',
      favicon:'icon.png',faviconType:'image/png'
    },
    'bocchi-agrobios':{
      slug:'bocchi-agrobios',client:'Bocchi Agrobios',shortName:'Bocchi',
      logoInstitutional:'assets/companies/bocchi-agrobios/logo-institucional.svg',
      logoDark:'logo-institucional.svg',logoLight:'logo-institucional.svg',
      favicon:'logo-institucional.svg'
    },
    'yvy-lab':{
      slug:'yvy-lab',client:'YvyLab',shortName:'YVY',
      logoInstitutional:'assets/companies/yvy-lab/logo-yvylab.png',
      logoDark:'logo-yvy-plus-escura.png',logoLight:'logo-yvy-plus-clara.png',
      favicon:'icon.png',faviconType:'image/png'
    },
    grazmec:{
      slug:'grazmec',client:'Grazmec',shortName:'Grazmec',
      logoInstitutional:'assets/companies/grazmec/logo-institucional.svg',
      logoDark:'logo-institucional.svg',logoLight:'logo-institucional.svg',
      favicon:'logo-institucional.svg'
    }
  });
  // Somente slugs registrados podem determinar caminhos de assets.
  const requested=new URLSearchParams(root.location.search).get('company');
  const available=Object.hasOwn(companies,requested);
  // A referência interna evita erros durante a navegação; nunca é exibida
  // nem inicializa ofertas quando o link não identifica uma empresa válida.
  const company=available?requested:'atsi-brasil';
  const config=companies[company];
  const assets=`assets/companies/${company}/`;
  const product=Object.freeze({
    ...config,company,assets,developer:'YvyLab',
    name:`${config.shortName}+`,
    slogan:'Conhecimento. Conexões. Oportunidades.',
    logoDark:assets+config.logoDark,logoLight:assets+config.logoLight,
    logoInstitutional:config.logoInstitutional || assets+config.logoDark,
    favicon:assets+config.favicon
  });
  function text(value){
    return String(value).replace(/ATSI\+|ATSI Brasil|\bATSI\b/g,match=>
      match==='ATSI+'?product.name:match==='ATSI Brasil'?product.client:product.shortName);
  }
  function copy(value){
    if(typeof value==='string')return text(value);
    if(Array.isArray(value))return value.map(copy);
    if(value && typeof value==='object')return Object.fromEntries(
      Object.entries(value).map(([key,item])=>[key,copy(item)]));
    return value;
  }
  function apply(container=document.body){
    if(!available)return;
    const walker=document.createTreeWalker(container,NodeFilter.SHOW_TEXT,{
      acceptNode(node){
        return node.parentElement.closest('script,style,textarea,input')?
          NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT;
      }
    });
    while(walker.nextNode()){
      const node=walker.currentNode;
      const branded=text(node.nodeValue);
      if(branded!==node.nodeValue)node.nodeValue=branded;
    }
    container.querySelectorAll('[data-company-logo]').forEach(image=>{
      const institutional=image.dataset.companyLogo==='institutional';
      image.src=institutional?product.logoInstitutional:product.logoDark;
      image.alt=institutional?product.client:product.name;
    });
    container.querySelectorAll('[data-company-heading]').forEach(heading=>{
      heading.textContent=product.name;
    });
  }
  function pageURL(path){
    const url=new URL(path,root.location.href);
    url.searchParams.set('company',company);
    return url;
  }
  // Preserva as campanhas existentes da ATSI; demais empresas têm chaves próprias.
  function storageKey(key){
    return company==='atsi-brasil'?key:`${key}:company:${company}`;
  }
  function pdfBranding(){
    const style=getComputedStyle(document.documentElement);
    const rgb=name=>style.getPropertyValue(name).trim().split(',').map(Number);
    return {header:rgb('--brand-header-rgb'),accent:rgb('--brand-accent-rgb')};
  }
  root.ATSIProduct=product;
  root.CompanyBranding=Object.freeze({available,text,copy,apply,pageURL,storageKey,pdfBranding});
  if(!available){
    document.documentElement.hidden=true;
    root.location.replace(new URL('404.html',document.baseURI));
    return;
  }
  document.documentElement.dataset.company=company;
  const theme=document.createElement('link');
  theme.rel='stylesheet';theme.href=assets+'theme.css';document.head.appendChild(theme);
  document.querySelector('link[rel="icon"]').href=product.favicon;
  document.querySelector('link[rel="icon"]').type=product.faviconType || 'image/svg+xml';
  document.title=text(document.title);
  document.querySelectorAll('meta[name="description"],meta[property="og:title"]').forEach(meta=>{
    meta.content=text(meta.content);
  });
})(globalThis);
